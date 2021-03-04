open Xi_lib
open Ast
(* W Xi_lib.Types są definicje typów i środowiska typowego *)
open Types

module Make() = struct

  (* Logger: używa się go jak Format.printf *)
  let logf fmt = Logger.make_logf __MODULE__ fmt

  module Check () = struct
    exception Exception of string

    (* Zgłaszaczka błędów *)
    module ErrorReporter = Typechecker_errors.MakeOneShotErrorReporter ()

    (* Hashtablica którą zwracamy jak wszystko jest OK.
     * Mapuje znacznik węzła na przypisany typ. Dzięki tej tablicy
     * późniejsze etapy kompilatora będą miały dostęp do policzonych
     * typów wyrażeń
     *
     * Jeżeli typowanie się powiedzie to zawartość tablicy wydrukuje się
     * do pliku xilog/004.typechecking.types
     *)
    let node2type_map = Hashtbl.create 513

    let rec type_to_normal_type = function
      | TEXPR_Int _ -> TP_Int
      | TEXPR_Bool _ -> TP_Bool
      | TEXPR_Array {sub; _} -> TP_Array (type_to_normal_type sub)

    (* --------------------------------------------------- *)
    (* Funkcja nakładka na inferencję, jej zadanie to uzupełniać hashtablicę node2type_map *)
    let rec infer_expression env e =
      let tp = _infer_expression env e in
      Hashtbl.replace node2type_map (tag_of_expression e) tp;
      logf "%s: inferred type %s"
        (string_of_location
        (location_of_expression e))
        (string_of_normal_type tp);
      tp

    (* --------------------------------------------------- *)
    (* Oddolna strategia *)
    and _infer_expression env = function
      | EXPR_Id {id; loc; _} ->
        (match TypingEnvironment.lookup id env with
        | None -> ErrorReporter.report_unknown_identifier ~loc ~id
        | Some environment_type ->
          (match environment_type with
          | ENVTP_Var normal_type -> normal_type
          | _ ->
            ErrorReporter.report_other_error ~loc ~descr:"Variable has type (extended_type * extended_type)."))

      | EXPR_Int _ ->
        TP_Int

      | EXPR_Char _ ->
        TP_Int

      | EXPR_Bool _ ->
        TP_Bool

      | EXPR_Index {expr;index;loc; _} ->
        (match infer_expression env expr with
        | TP_Array array_type ->
          (match infer_expression env index with
          | TP_Int -> array_type
          | index_type -> ErrorReporter.report_type_mismatch ~loc ~expected:TP_Int ~actual:index_type)
        | subexpression_type -> ErrorReporter.report_expected_array ~loc ~actual:subexpression_type)

      | EXPR_Call call ->
        check_function_call env call

      | EXPR_Length {arg;loc;_} ->
        (match infer_expression env arg with
        | TP_Array _ -> TP_Int
        | argument_type -> ErrorReporter.report_expected_array ~loc ~actual:argument_type)

      | EXPR_Relation {lhs; rhs; op=RELOP_Ge; loc; _}
      | EXPR_Relation {lhs; rhs; op=RELOP_Gt; loc; _}
      | EXPR_Relation {lhs; rhs; op=RELOP_Lt; loc; _}
      | EXPR_Relation {lhs; rhs; op=RELOP_Le; loc; _}  ->
        check_expression env TP_Int lhs;
        check_expression env TP_Int rhs;
        TP_Bool

      | EXPR_Relation {lhs; rhs; op=RELOP_Eq; loc; _}
      | EXPR_Relation {lhs; rhs; op=RELOP_Ne; loc; _} ->
        let lhs_type = infer_expression env lhs in
        check_expression env lhs_type rhs;
        TP_Bool

        (* Reguła dla dodawania, jak w treści zadania *)
      | EXPR_Binop {loc; lhs; rhs; op=BINOP_Add; _} ->
        begin match infer_expression env lhs with
        | (TP_Array _) as tp
        | (TP_Int as tp) ->
          check_expression env tp rhs;
          tp
        | _ ->
          let descr = "operator + expects integer or array" in
         ErrorReporter.report_other_error ~loc ~descr
        end

      | EXPR_Binop {lhs; rhs; op=BINOP_And;_}
      | EXPR_Binop {lhs; rhs; op=BINOP_Or; _} ->
        check_expression env TP_Bool lhs;
        check_expression env TP_Bool rhs;
        TP_Bool

      | EXPR_Binop {lhs; rhs; op=BINOP_Sub;_}
      | EXPR_Binop {lhs; rhs; op=BINOP_Rem;_}
      | EXPR_Binop {lhs; rhs; op=BINOP_Mult;_}
      | EXPR_Binop {lhs; rhs; op=BINOP_Div; _} ->
        check_expression env TP_Int lhs;
        check_expression env TP_Int lhs;
        TP_Bool

      | EXPR_Unop {op=UNOP_Neg; sub; _} ->
        check_expression env TP_Int sub;
        TP_Int

      | EXPR_Unop {op=UNOP_Not; sub; _} ->
        check_expression env TP_Bool sub;
        TP_Bool

      | EXPR_String _ ->
        TP_Array TP_Int

      | EXPR_Struct {elements=[]; loc; _} ->
        ErrorReporter.report_cannot_infer ~loc

      | EXPR_Struct {elements=x::xs; _} ->
        let first_element_type = infer_expression env x in
        List.iter (check_expression env first_element_type) xs;
        TP_Array first_element_type

    and check_function_call env (Call {tag; loc; callee; arguments}) =
      let check_arguments parameters_types arguments =
        let parameters_count = List.length parameters_types in
        let arguments_count = List.length arguments in
        if parameters_count <> arguments_count
        then ErrorReporter.report_bad_number_of_arguments ~loc ~expected:parameters_count ~actual:arguments_count
        else let rec aux parameters_types arguments =
            match (parameters_types, arguments) with
            | [], [] -> ()
            | expected :: ts, arg :: args ->
              let actual = infer_expression env arg in
              if actual == expected then aux ts args
              else ErrorReporter.report_type_mismatch ~loc:(location_of_expression arg) ~expected ~actual
            | _ -> ErrorReporter.report_other_error ~loc ~descr:"This should never happen; wrong arguments count, but I've checked for it before" in
          aux parameters_types arguments in
      match TypingEnvironment.lookup callee env with
      | None -> ErrorReporter.report_unknown_identifier ~loc ~id:callee
      | Some environment_type -> (match environment_type with
        | ENVTP_Var _ -> ErrorReporter.report_other_error ~loc ~descr:"Function has type normal_type (instead of extended_type * extended_type)"
        | ENVTP_Fn (parameters_types, return_types) ->
          (match return_types with
          | [] -> ErrorReporter.report_other_error ~loc ~descr:"Function returns ()"
          | [normal_type] ->
            check_arguments parameters_types arguments;
            normal_type
          | _ -> ErrorReporter.report_other_error ~loc ~descr:"Function returns too many values"))

    (* --------------------------------------------------- *)
    (* Odgórna strategia: zapish w node2type_map oczekiwanie a następnie
     * sprawdź czy nie zachodzi specjalny przypadek. *)
    and check_expression env expected e =
      logf "%s: checking expression against %s"
        (string_of_location (location_of_expression e))
        (string_of_normal_type expected);
      Hashtbl.replace node2type_map (tag_of_expression e) expected;

      (* Sprawdzamy specjalne przypadki *)
      match e, expected with
          (* Mamy sprawdzić `{elements...}` kontra `tp[]`, czyli sprawdzamy
          * elementy kontra typ elementu tablicy `tp` *)
      | EXPR_Struct {elements; _}, TP_Array tp ->
        List.iter (check_expression env tp) elements

      (* ========== !! Zaimplementuj pozostale przypadki !! =========  *)

      (* Fallback do strategii oddolnej *)
      | _ ->
        let actual = infer_expression env e in
        if actual <> expected then
          ErrorReporter.report_type_mismatch
            ~loc:(location_of_expression e)
            ~actual
            ~expected

    (* --------------------------------------------------- *)
    (* Pomocnicza funkcja do sprawdzania wywołania procedury *)

    let check_procedure_call env (Call {tag; loc; callee; arguments}) : unit =
      let check_arguments parameters_types arguments =
        let parameters_count = List.length parameters_types in
        let arguments_count = List.length arguments in
        if parameters_count <> arguments_count
        then ErrorReporter.report_bad_number_of_arguments ~loc ~expected:parameters_count ~actual:arguments_count
        else let rec aux parameters_types arguments =
            match (parameters_types, arguments) with
            | [], [] -> ()
            | expected :: ts, arg :: args ->
              let actual = infer_expression env arg in
              if actual == expected then aux ts args
              else ErrorReporter.report_type_mismatch ~loc:(location_of_expression arg) ~expected ~actual
            | _ -> ErrorReporter.report_other_error ~loc ~descr:"This should never happen; wrong arguments count, but I've checked for it before" in
          aux parameters_types arguments in
      match TypingEnvironment.lookup callee env with
      | None -> ErrorReporter.report_unknown_identifier ~loc ~id:callee
      | Some environment_type -> (match environment_type with
        | ENVTP_Var _ -> ErrorReporter.report_other_error ~loc ~descr:"Function has type normal_type (instead of extended_type * extended_type)"
        | ENVTP_Fn (parameters_types, return_types) ->
          (match return_types with
          | [] -> ()
          | _ -> ErrorReporter.report_other_error ~loc ~descr:"Procedure returns some values"))

    (* --------------------------------------------------- *)
    (* Rekonstrukcja typu dla lvalue *)

    let infer_lvalue env = function
      | LVALUE_Id {id;loc;_} ->
        (match TypingEnvironment.lookup id env with
        | None -> ErrorReporter.report_unknown_identifier ~loc ~id
        | Some environment_type -> (match environment_type with
          | ENVTP_Var normal_type -> normal_type
          | ENVTP_Fn _ -> ErrorReporter.report_other_error ~loc ~descr:"lvalue has type extended_type * extended_type."))

      | LVALUE_Index {index; sub; loc} ->
        (match infer_expression env sub with
        | TP_Array array_type ->
          (match infer_expression env index with
          | TP_Int -> array_type
          | index_type -> ErrorReporter.report_type_mismatch ~loc ~expected:TP_Int ~actual:index_type)
        | subexpression_type -> ErrorReporter.report_expected_array ~loc ~actual:subexpression_type)


    (* --------------------------------------------------- *)
    (* Sprawdzanie statementów *)

    let rec check_statement env = function
      (* Proste, wyinferuj typ `lhs` i sprawdź `rhs` kontra wynik *)
      | STMT_Assign {lhs; rhs; _} ->
        let lhs_tp = infer_lvalue env lhs in
        check_expression env lhs_tp rhs;
        env, RT_Unit

      | STMT_MultiVarDecl {vars; init; _} ->
        let rec aux variable_declarations_list return_types_list env =
          (match (variable_declarations_list, return_types_list) with
          | [], [] -> env, RT_Unit
          | None :: vs, expected :: ts -> aux vs ts env
          | Some (VarDecl {loc; tp; id}) :: vs, expected :: ts ->
            let actual = type_to_normal_type tp in
            if actual == expected
            then (match TypingEnvironment.add id (ENVTP_Var actual) env with
              | env, false -> ErrorReporter.report_shadows_previous_definition ~loc ~id
              | env, true -> aux vs ts env)
            else ErrorReporter.report_type_mismatch ~loc ~expected ~actual
          | _ -> raise (Exception "This should never happen; wrong variables count, but I've checked for it before")) in
        let unused_value = check_function_call env init in
        (match init with Call {loc; callee; _} ->
          (match TypingEnvironment.lookup callee env with
          | None -> ErrorReporter.report_unknown_identifier ~loc ~id:callee
          | Some environment_type -> (match environment_type with
            | ENVTP_Var _ -> ErrorReporter.report_other_error ~loc ~descr:"Function has type normal_type (instead of extended_type * extended_type)"
            | ENVTP_Fn (_, return_types) ->
              (match return_types with
              | []
              | [_] -> ErrorReporter.report_other_error ~loc ~descr:"Multi-return function returns () or 1 value"
              | ts -> aux vars ts env))))

      | STMT_Block body ->
        check_statement_block env body

      | STMT_Call call ->
        check_procedure_call env call;
        env, RT_Unit

      | STMT_If {cond;then_branch;else_branch; loc} ->
        check_expression env TP_Bool cond;
        (match else_branch with
        | None -> check_statement env then_branch
        | Some statement -> (match check_statement env then_branch with
          | _, RT_Unit -> (match check_statement env statement with
            | _, RT_Unit -> env, RT_Unit
            | _, RT_Void -> ErrorReporter.report_other_error ~loc ~descr:"Else branch should return unit, but returns void")
          | _, RT_Void -> (match check_statement env statement with
            | _, RT_Unit -> ErrorReporter.report_other_error ~loc ~descr:"Else branch should return void, but returns unit"
            | _, RT_Void -> env, RT_Void)))

      | STMT_Return {values;loc} ->
        env, RT_Void

      | STMT_VarDecl {var; init} ->
        (match var with VarDecl {loc; id; tp} ->
          (match init with
          | None -> (match TypingEnvironment.add id (ENVTP_Var (type_to_normal_type tp)) env with
            | _, false -> ErrorReporter.report_shadows_previous_definition ~loc ~id
            | env, true -> env, RT_Unit)
          | Some expression -> let expected = type_to_normal_type tp in
            let actual = infer_expression env expression in
            if expected == actual
            then (match TypingEnvironment.add id (ENVTP_Var (type_to_normal_type tp)) env with
              | _, false -> ErrorReporter.report_shadows_previous_definition ~loc ~id
              | env, true -> env, RT_Unit)
            else ErrorReporter.report_type_mismatch ~loc ~expected ~actual))

      | STMT_While {cond; body; _} ->
        check_expression env TP_Bool cond;
        check_statement env body

    and check_statement_block env (STMTBlock {body; _}) =
        failwith "not yet implemented"

    (* --------------------------------------------------- *)
    (* Top-level funkcje *)

    let check_global_declaration env = function
      | GDECL_Function {formal_parameters; return_types; body; loc; id; _} ->
        (* Sprawdź wszystko *)
        failwith "not yet implemented"

    let scan_global_declaration env = function
      | GDECL_Function {id; formal_parameters; return_types; loc; _} ->
        (* Dodaj idenetyfkator funkcji i jej typ do środowiska *)
        let arguments_types = List.map type_expression_of_var_declaration formal_parameters in
        let arguments_normal_types = List.map type_to_normal_type arguments_types in
        let normal_return_types = List.map type_to_normal_type return_types in
        match TypingEnvironment.add id (ENVTP_Fn (arguments_normal_types, normal_return_types)) env with
        | _, false -> ErrorReporter.report_shadows_previous_definition ~loc ~id
        | env, true -> env

    let scan_module env (ModuleDefinition {global_declarations; _}) =
      List.fold_left scan_global_declaration env global_declarations

    let check_module env (ModuleDefinition {global_declarations; _}) =
      List.iter (check_global_declaration env) global_declarations

    (* --------------------------------------------------- *)
    (* Przetwórz moduł *)
    let process_module env mdef =
      (* Wpierw przeskanuj globalne definicje aby uzupełnić środowisko *)
      let env = scan_module env mdef in
      (* Zweryfikuj wszystko *)
      check_module env mdef

    let computation mdef =
      (* Zaczynamy z pustym środowiskiem *)
      let env = TypingEnvironment.empty in
      process_module env mdef;
      node2type_map
  end

  (* --------------------------------------------------- *)
  (* Procedura wejściowa *)
  let check_module mdef =
    (* Stwórz instancję typecheckera i ją odpal *)
    let module M = Check() in
    M.ErrorReporter.wrap M.computation mdef

end
