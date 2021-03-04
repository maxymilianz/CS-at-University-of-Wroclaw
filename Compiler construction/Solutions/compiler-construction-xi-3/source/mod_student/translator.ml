open Xi_lib
open Ir

let i32_0 = Int32.of_int 0
let i32_1 = Int32.of_int 1

(* --------------------------------------------------- *)

module Make() = struct

  module Environment = struct

    type env = Env of
      { procmap: procid Ast.IdMap.t
      ; varmap: reg Ast.IdMap.t
      }

    let empty =
      let procmap = Ast.IdMap.empty in
      let varmap = Ast.IdMap.empty in
      Env {procmap; varmap}


    let add_proc id procid (Env {procmap; varmap}) =
      let procmap = Ast.IdMap.add id procid procmap in
      Env {procmap; varmap}

    let add_var id reg (Env {procmap; varmap}) =
      let varmap = Ast.IdMap.add id reg varmap in
      Env {procmap; varmap}

    let lookup_proc id (Env {procmap; _}) =
      try
        Ast.IdMap.find id procmap
      with Not_found ->
        failwith @@ Format.sprintf "Unknown procedure identifier: %s" (Ast.string_of_identifier id)

    let lookup_var id (Env {varmap; _}) =
      try
        Ast.IdMap.find id varmap
      with Not_found ->
        failwith @@ Format.sprintf "Unknown variable identifier: %s" (Ast.string_of_identifier id)

  end


(* --------------------------------------------------- *)
  module Scanner = struct

    let mangle_id id =
      Format.sprintf "_I_%s" (Ast.string_of_identifier id)

    let rec mangle_texpr = function
      | Ast.TEXPR_Int _ -> "i"
      | Ast.TEXPR_Bool _ -> "b"
      | Ast.TEXPR_Array {sub;_} -> "a" ^ mangle_texpr sub


    let mangle_var_declaration v = mangle_texpr @@ Ast.type_expression_of_var_declaration v

    let mangle_formal_parameters xs = String.concat "" (List.map mangle_var_declaration xs)

    let mangle_return_types xs = String.concat "" (List.map mangle_texpr xs)

    let scan_global_declaration (env, symbols) = function
      | Ast.GDECL_Function {id; formal_parameters; return_types; _} ->
        let name = Format.sprintf "%s_%s_%s"
          (mangle_id id) (mangle_formal_parameters formal_parameters) (mangle_return_types return_types)
          in

        Environment.add_proc id (Procid name) env, Procid name :: symbols

    let scan_module env (Ast.ModuleDefinition {global_declarations; _}) =
      List.fold_left scan_global_declaration (env, []) global_declarations

  end
(* --------------------------------------------------- *)

  module type SContext = sig

    val cfg : ControlFlowGraph.t

    val node2type: (Ast.node_tag, Types.normal_type) Hashtbl.t

    val allocate_register: unit -> reg
  end

(* --------------------------------------------------- *)
  module Translator(M:SContext) = struct
    open M

    (* dodaj instrukcje do bloku *)
    let append_instruction l i =
      let block = ControlFlowGraph.block cfg l in
      ControlFlowGraph.set_block cfg l (block @ [i])

    (* ustaw terminator na skok bezwarunkowy *)
    let set_jump l_from l_to =
      ControlFlowGraph.set_terminator cfg l_from @@ T_Jump l_to;
      ControlFlowGraph.connect cfg l_from l_to

    (* ustaw terminator na powrót-z-procedury *)
    let set_return l_from xs =
      ControlFlowGraph.set_terminator cfg l_from @@ T_Return xs;
      ControlFlowGraph.connect cfg l_from (ControlFlowGraph.exit_label cfg)

    (* ustaw terminator na skok warunkowy *)
    let set_branch cond a b l_from l_to1 l_to2 =
      ControlFlowGraph.set_terminator cfg l_from @@ T_Branch (cond, a, b, l_to1, l_to2);
      ControlFlowGraph.connect cfg l_from l_to1;
      ControlFlowGraph.connect cfg l_from l_to2

    let allocate_block () = ControlFlowGraph.allocate_block cfg

    let i32_0 = Int32.of_int 0
    let i32_1 = Int32.of_int 1

    (* --------------------------------------------------- *)
    let rec translate_expression env current_bb = function
      | Ast.EXPR_Char {value; _} ->
        current_bb, E_Int (Int32.of_int @@ Char.code value)

      | Ast.EXPR_Id {id; _} ->
        current_bb, E_Reg (Environment.lookup_var id env)

      | Ast.EXPR_Int {value; _} ->
        current_bb, E_Int value

      | Ast.EXPR_String {value; _} ->
        let register = allocate_register () in
        let length = String.length value in
        append_instruction current_bb (I_NewArray (register, (E_Int (Int32.of_int length))));
        let register = E_Reg register in
        let rec save_string_to_array i =
          if i == length then ()
          else
            let index = E_Int (Int32.of_int i) in
            let element = E_Int (Int32.of_int (Char.code (String.get value i))) in
            append_instruction current_bb (I_StoreArray (register, index, element));
            save_string_to_array (i + 1) in
        save_string_to_array 0;
        current_bb, register

      | Ast.EXPR_Bool {value; _} ->
        (match value with
        | false -> current_bb, E_Int i32_0
        | true -> current_bb, E_Int i32_1)

      | Ast.EXPR_Relation {op; lhs; rhs; _} ->
        let current_bb, lhs_expr = translate_expression env current_bb lhs in
        let current_bb, rhs_expr = translate_expression env current_bb rhs in
        let register = allocate_register () in
        let cond = match op with
          | RELOP_Eq -> COND_Eq
          | RELOP_Ne -> COND_Ne
          | RELOP_Lt -> COND_Lt
          | RELOP_Le -> COND_Le
          | RELOP_Gt -> COND_Gt
          | RELOP_Ge -> COND_Ge in
        let false_bb = allocate_block () in
        let true_bb = allocate_block () in
        set_branch cond lhs_expr rhs_expr current_bb true_bb false_bb;
        append_instruction false_bb (I_Move (register, E_Int i32_0));
        append_instruction true_bb (I_Move (register, E_Int i32_1));
        let final_bb = allocate_block () in
        set_jump false_bb final_bb;
        set_jump true_bb final_bb;
        final_bb, E_Reg register

      | Ast.EXPR_Binop {op = BINOP_And; lhs; rhs; _}
      | Ast.EXPR_Binop {op = BINOP_Or; lhs; rhs; _} as expr ->
        let register = allocate_register () in
        let else_bb = allocate_block () in
        let true_bb = translate_condition env current_bb else_bb expr in
        append_instruction true_bb (I_Move (register, E_Int (i32_1)));
        append_instruction else_bb (I_Move (register, E_Int (i32_0)));
        let final_bb = allocate_block () in
        set_jump true_bb final_bb;
        set_jump else_bb final_bb;
        final_bb, E_Reg register

      | Ast.EXPR_Binop {op; lhs; rhs; _} ->
        let current_bb, lhs_expr = translate_expression env current_bb lhs in
        let current_bb, rhs_expr = translate_expression env current_bb rhs in
        let register = allocate_register () in
        let instruction = match op with
          | BINOP_And | BINOP_Or as c ->
            failwith "Should never happen; was checked before"
          | BINOP_Add ->
            let rec lhs_aux expr = (match expr with
              | Ast.EXPR_Id _
              | Ast.EXPR_Call _ -> None
              | Ast.EXPR_Int _
              | Ast.EXPR_Char _
              | Ast.EXPR_Bool _
              | Ast.EXPR_Relation _
              | Ast.EXPR_Length _
              | Ast.EXPR_Unop _ -> Some (I_Add (register, lhs_expr, rhs_expr))
              | Ast.EXPR_Binop {op; lhs; rhs; _} -> (match op with
                | Ast.BINOP_Add -> (match lhs_aux lhs with
                  | None -> lhs_aux rhs
                  | some_instruction -> some_instruction)
                | _ -> Some (I_Add (register, lhs_expr, rhs_expr)))
              | Ast.EXPR_Index {expr; _} -> lhs_aux expr
              | Ast.EXPR_Struct _
              | Ast.EXPR_String _ -> Some (I_Concat (register, lhs_expr, rhs_expr)))
            and rhs_aux expr = (match expr with
              | Ast.EXPR_Id _
              | Ast.EXPR_Call _ -> I_Add (register, lhs_expr, rhs_expr)
              | Ast.EXPR_Int _
              | Ast.EXPR_Char _
              | Ast.EXPR_Bool _
              | Ast.EXPR_Relation _
              | Ast.EXPR_Length _
              | Ast.EXPR_Unop _ -> I_Add (register, lhs_expr, rhs_expr)
              | Ast.EXPR_Binop {op; lhs; _} -> (match op with
                | Ast.BINOP_Add -> rhs_aux lhs
                | _ -> I_Add (register, lhs_expr, rhs_expr))
              | Ast.EXPR_Index {expr; _} -> rhs_aux expr
              | Ast.EXPR_Struct _
              | Ast.EXPR_String _ -> I_Concat (register, lhs_expr, rhs_expr)) in
            (match lhs_aux lhs with
            | None -> rhs_aux lhs
            | Some instruction -> instruction)
          | BINOP_Sub -> I_Sub (register, lhs_expr, rhs_expr)
          | BINOP_Mult -> I_Mul (register, lhs_expr, rhs_expr)
          | BINOP_Div -> I_Div (register, lhs_expr, rhs_expr)
          | BINOP_Rem -> I_Rem (register, lhs_expr, rhs_expr) in
        append_instruction current_bb instruction;
        current_bb, E_Reg register

      | Ast.EXPR_Length {arg; _} ->
        let current_bb, arg_expr = translate_expression env current_bb arg in
        let register = allocate_register () in
        append_instruction current_bb (I_Length (register, arg_expr));
        current_bb, E_Reg register

      | Ast.EXPR_Unop {op; sub; _} ->
        let current_bb, sub_expr = translate_expression env current_bb sub in
        let register = allocate_register () in
        let instruction = match op with
          | UNOP_Not -> I_Not (register, sub_expr)
          | UNOP_Neg -> I_Neg (register, sub_expr) in
        append_instruction current_bb instruction;
        current_bb, E_Reg register

      | Ast.EXPR_Call (Ast.Call {callee; arguments; _}) ->
        let procid = Environment.lookup_proc callee env in
        let rec aux current_bb result = function
          | [] -> current_bb, result
          | first_argument :: arguments ->
            let current_bb, first_argument_expr = translate_expression env current_bb first_argument in
            aux current_bb (result @ [first_argument_expr]) arguments in
        let current_bb, arguments_exprs = aux current_bb [] arguments in
        let register = allocate_register () in
        append_instruction current_bb (I_Call ([register], procid, arguments_exprs, []));
        current_bb, E_Reg register

      | Ast.EXPR_Index {expr; index; _} ->
        let current_bb, expr_expr = translate_expression env current_bb expr in
        let current_bb, index_expr = translate_expression env current_bb index in
        let register = allocate_register () in
        append_instruction current_bb (I_LoadArray (register, expr_expr, index_expr));
        current_bb, E_Reg register

      | Ast.EXPR_Struct {elements; _} ->
        let length = List.length elements in
        let register =  allocate_register () in
        let register_expr = E_Reg register in
        append_instruction current_bb (I_NewArray (register, (E_Int (Int32.of_int length))));
        let rec store_array current_bb i =
          if i == length then current_bb
          else
            let current_bb, element_expr = translate_expression env current_bb (List.nth elements i) in
            append_instruction current_bb (I_StoreArray (register_expr, (E_Int (Int32.of_int i)), element_expr));
            store_array current_bb (i + 1) in
        store_array current_bb 0, register_expr

    (* --------------------------------------------------- *)
    and translate_condition env current_bb else_bb = function
      | Ast.EXPR_Bool {value=true; _} ->
        current_bb

      | Ast.EXPR_Bool {value=false; _} ->
        set_jump current_bb else_bb;
        allocate_block ()

      | Ast.EXPR_Binop {op = BINOP_And; lhs; rhs; _} ->
        let first_bb = translate_condition env current_bb else_bb lhs in
        translate_condition env first_bb else_bb rhs

      | Ast.EXPR_Binop {op = BINOP_Or; lhs; rhs; _} ->
        let false_bb = allocate_block () in
        let first_bb = translate_condition env current_bb false_bb lhs in
        let second_bb = translate_condition env false_bb else_bb rhs in
        let true_bb = allocate_block () in
        set_jump first_bb true_bb;
        set_jump second_bb true_bb;
        true_bb

      | e ->
        let current_bb, res = translate_expression env current_bb e in
        let next_bb = allocate_block () in
        set_branch COND_Ne res (E_Int i32_0) current_bb next_bb else_bb;
        next_bb


    (* --------------------------------------------------- *)

    let rec translate_statement env current_bb = function
      | Ast.STMT_Call (Call {callee; arguments; _}) ->
        let procid = Environment.lookup_proc callee env in
        let rec aux current_bb result = function
          | [] -> current_bb, result
          | first_argument :: arguments ->
            let current_bb, first_argument_expr = translate_expression env current_bb first_argument in
            aux current_bb (result @ [first_argument_expr]) arguments in
        let current_bb, arguments_exprs = aux current_bb [] arguments in
        append_instruction current_bb (I_Call ([], procid, arguments_exprs, []));
        env, current_bb

      | Ast.STMT_Assign {lhs; rhs; _} ->
        let current_bb, rhs_expr = translate_expression env current_bb rhs in
        (match lhs with
          | LVALUE_Id {id; _} ->
            append_instruction current_bb (I_Move (Environment.lookup_var id env, rhs_expr));
            env, current_bb
          | LVALUE_Index {sub; index; _} ->
            let current_bb, sub_expr = translate_expression env current_bb sub in
            let current_bb, index_expr = translate_expression env current_bb index in
            append_instruction current_bb (I_StoreArray (sub_expr, index_expr, rhs_expr));
            env, current_bb)

      | Ast.STMT_VarDecl {var = VarDecl {id; tp; _}; init} ->
        let register = allocate_register () in
        let current_bb = (match tp with
          | Ast.TEXPR_Int _
          | Ast.TEXPR_Bool _ -> current_bb
          | Ast.TEXPR_Array {sub; dim; _} -> let rec aux current_bb = (function
            | Ast.TEXPR_Int _
            | Ast.TEXPR_Bool _ -> current_bb, Some (E_Int i32_1)
            | Ast.TEXPR_Array {sub; dim; _} -> match dim with
              | None -> current_bb, None
              | Some expr ->
                match aux current_bb sub with
                | current_bb, None -> current_bb, None
                | current_bb, Some sub_expr ->
                  let current_bb, expr_expr = translate_expression env current_bb expr in
                  let register = allocate_register () in
                  append_instruction current_bb (I_Mul (register, expr_expr, sub_expr));
                  current_bb, Some (E_Reg register)) in
            match dim with
            | None -> current_bb
            | Some expr ->
              let current_bb, size_expr = aux current_bb sub in
              (match size_expr with
              | None -> current_bb
              | Some size_expr ->
                let current_bb, expr_expr = translate_expression env current_bb expr in
                let size_register = allocate_register () in
                append_instruction current_bb (I_Mul (size_register, expr_expr, size_expr));
                append_instruction current_bb (I_NewArray (register, E_Reg size_register));
                current_bb)) in
        let env = Environment.add_var id register env in
        (match init with
        | None -> env
        | Some expr ->
          let _, expr_expr = translate_expression env current_bb expr in
          append_instruction current_bb (I_Move (register, expr_expr));
          env), current_bb

      | Ast.STMT_If {cond; then_branch; else_branch; _} ->
        let else_bb = allocate_block () in
        let then_bb = translate_condition env current_bb else_bb cond in
        let env, then_bb = translate_statement env then_bb then_branch in
        let env, else_bb = match else_branch with
          | None -> env, else_bb
          | Some statement -> translate_statement env else_bb statement in
        let final_bb = allocate_block () in
        set_jump then_bb final_bb;
        set_jump else_bb final_bb;
        env, final_bb

      | Ast.STMT_While {cond; body; _} ->
        let cond_bb = allocate_block () in
        let false_bb = allocate_block () in
        let body_bb = translate_condition env cond_bb false_bb cond in
        let _, body_bb = translate_statement env body_bb body in
        set_jump current_bb cond_bb;
        set_jump body_bb cond_bb;
        env, false_bb

      | Ast.STMT_Return {values; _} ->
        let rec aux current_bb result = function
          | [] -> current_bb, result
          | first_value :: values ->
            let current_bb, first_value_expr = translate_expression env current_bb first_value in
            aux current_bb (result @ [first_value_expr]) values in
        let current_bb, values_exprs = aux current_bb [] values in
        set_return current_bb values_exprs;
        env, allocate_block ()

      | Ast.STMT_MultiVarDecl {vars; init = (Call {callee; arguments; _}); _} ->
        let rec aux env result = function
          | [] -> env, result
          | first_var :: vars -> match first_var with
            | None -> aux env (allocate_register () :: result) vars
            | Some (Ast.VarDecl {id; _}) ->
              let register = allocate_register () in
              let env = Environment.add_var id register env in
              aux env (register :: result) vars in
        let procid = Environment.lookup_proc callee env in
        let rec aux_1 current_bb result = function
          | [] -> current_bb, result
          | first_argument :: arguments ->
            let current_bb, first_argument_expr = translate_expression env current_bb first_argument in
            aux_1 current_bb (result @ [first_argument_expr]) arguments in
        let current_bb, arguments_exprs = aux_1 current_bb [] arguments in
        let env, vars_exprs = aux env [] vars in
        append_instruction current_bb (I_Call (vars_exprs, procid, arguments_exprs, []));
        env, current_bb

      | Ast.STMT_Block block -> translate_block env current_bb block


    and translate_block env current_bb (Ast.STMTBlock {body; _}) =
      let rec aux env current_bb = function
        | [] -> env, current_bb
        | first_statement :: body ->
          let env, current_bb = translate_statement env current_bb first_statement in
          aux env current_bb body in
      aux env current_bb body

    let bind_var_declaration env vardecl =
      let r = allocate_register () in
      let env = Environment.add_var (Ast.identifier_of_var_declaration vardecl) r env in
      env, r

    let bind_formal_parameters env xs =
      let f env x = fst (bind_var_declaration env x) in
      List.fold_left f env xs

  let translate_global_definition env = function
    | Ast.GDECL_Function {id; body=Some body; formal_parameters;_} ->
      let procid = Environment.lookup_proc id env in
      let frame_size = 0 in
      let env = bind_formal_parameters env formal_parameters in
      let formal_parameters = List.length formal_parameters in
      let proc = Procedure {procid; cfg; frame_size; allocate_register; formal_parameters} in
      let first_bb = allocate_block () in
      let _, last_bb = translate_block env first_bb body in
      ControlFlowGraph.connect cfg  last_bb (ControlFlowGraph.exit_label cfg);
      ControlFlowGraph.connect cfg  (ControlFlowGraph.entry_label cfg) first_bb;
      [proc]

    | _ ->
      []

  end

  let make_allocate_register () =
    let counter = ref 0 in
    fun () ->
      let i = !counter in
      incr counter;
      REG_Tmp i


    let translate_global_definition node2type env gdef =
      let cfg = ControlFlowGraph.create () in
      let module T = Translator(struct
        let cfg = cfg
        let node2type = node2type
        let allocate_register = make_allocate_register ()
      end) in
      T.translate_global_definition env gdef

    let translate_module node2type env (Ast.ModuleDefinition {global_declarations; _}) =
      List.flatten @@ List.map (translate_global_definition node2type env) global_declarations

    let translate_module mdef node2type =
      let env = Environment.empty in
      let env, symbols = Scanner.scan_module env mdef in
      let procedures = translate_module node2type env mdef in
      Program {procedures; symbols}
  end
