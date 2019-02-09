open Xi_lib
open Ir
open Ir_utils

module Make() = struct

  module Implementation(M:sig
      val cfg: ControlFlowGraph.t
      val initial: Analysis_domain.ConstantFolding.domain
    end) = struct

    open M

    let result = Hashtbl.create 513

    let sum_bindings _ maybe_binding_0 maybe_binding_1 =
        match maybe_binding_0, maybe_binding_1 with
        | None, binding
        | binding, None -> binding
        | Some binding_0, Some binding_1 -> Some (match binding_0, binding_1 with
            | None, value
            | value, None -> None
            | Some value_0, Some value_1 ->
                if value_0 == value_1 then Some value_0
                else Some None)

    let sum_knowledge registers_map = function
        | None -> registers_map
        | Some block_knowledge ->
            let post = Analysis.BlockKnowledge.post block_knowledge in
            (* Ir.RegMap.merge sum_bindings registers_map post *)
            let aux register binding_0 registers_map =
                match Ir.RegMap.find_opt register registers_map with
                | None -> Ir.RegMap.add register binding_0 registers_map
                | Some binding_1 -> match binding_0, binding_1 with
                    | None, value
                    | value, None -> Ir.RegMap.add register None registers_map
                    | Some value_0, Some value_1 ->
                        if value_0 == value_1 then registers_map
                        else Ir.RegMap.add register None registers_map in
            Ir.RegMap.fold aux post registers_map

    let value_of_expression expression pre = match expression with
        | E_Reg register -> (match Ir.RegMap.find_opt register pre with
            | None -> None
            | Some value -> value)
        | E_Int value -> Some value

    let interpret_instruction instruction integer_0 integer_1 =
        match instruction with
            | I_Add _ -> Some (Int32.of_int ((+) integer_0 integer_1))
            | I_Sub _ -> Some (Int32.of_int ((-) integer_0 integer_1))
            | I_Div _ -> if integer_1 == 0 then None
                else Some (Int32.of_int ((/) integer_0 integer_1))
            | I_Rem _ -> Some (Int32.of_int ((mod) integer_0 integer_1))
            | I_Mul _ -> Some (Int32.of_int (( * ) integer_0 integer_1))
            | I_And _ -> Some (Int32.of_int ((land) integer_0 integer_1))
            | I_Or _ -> Some (Int32.of_int ((lor) integer_0 integer_1))
            | I_Xor _ -> Some (Int32.of_int ((lxor) integer_0 integer_1))
            | _ -> failwith "Wrong argument"

    let register_number = function
        | REG_Tmp number
        | REG_Hard number
        | REG_Spec number -> number

    let interpret_unary operator integer = match operator with
        | I_Neg _ -> Some (Int32.of_int (-integer))
        | I_Not _ -> Some (Int32.of_int (lnot integer))
        | _ -> failwith "Wrong argument"

    let add_used_registers registers_map register =
        Ir.RegMap.add register None registers_map

    let interpret_condition condition integer_0 integer_1 =
        let int_of_bool = function
            | false -> Some (Int32.of_int 0)
            | true -> Some (Int32.of_int 1) in
        let operation = match condition with
            | COND_Eq -> (==)
            | COND_Ne -> (<>)
            | COND_Lt -> (<)
            | COND_Gt -> (>)
            | COND_Le -> (<=)
            | COND_Ge -> (>=) in
        int_of_bool (operation integer_0 integer_1)

    let transfer_instruction instruction pre = match instruction with
        | I_Add (register, expression_0, expression_1)
        | I_Sub (register, expression_0, expression_1)
        | I_Div (register, expression_0, expression_1)
        | I_Rem (register, expression_0, expression_1)
        | I_Mul (register, expression_0, expression_1)
        | I_And (register, expression_0, expression_1)
        | I_Or (register, expression_0, expression_1)
        | I_Xor (register, expression_0, expression_1) as interpretable_instruction ->
            let value_0 = value_of_expression expression_0 pre in
            let value_1 = value_of_expression expression_1 pre in
            let value = match value_0, value_1 with
                | None, _
                | _, None -> None
                | Some integer_0, Some integer_1 -> interpret_instruction interpretable_instruction (Int32.to_int integer_0) (Int32.to_int integer_1) in
            let post = Ir.RegMap.add register value pre in
            post
        | I_LoadArray (register, _, _)
        | I_LoadMem (register, _, _)
        | I_Concat (register, _, _) ->
            let post = Ir.RegMap.add register None pre in
            post
        | I_Neg (register, expression)
        | I_Not (register, expression) as interpratable_unary ->
            let value = match value_of_expression expression pre with
                | None -> None
                | Some integer -> interpret_unary interpratable_unary (Int32.to_int integer) in
            let post = Ir.RegMap.add register value pre in
            post
        | I_Move (register, expression) ->
            let value = value_of_expression expression pre in
            let post = Ir.RegMap.add register value pre in
            post
        | I_Length (register, _)
        | I_NewArray (register, _) ->
            let post = Ir.RegMap.add register None pre in
            post
        | I_Call (target_registers, _, _, modified_registers) ->
            let post = List.fold_left add_used_registers pre (target_registers @ modified_registers) in
            post
        | I_Set (register, condition, expression_0, expression_1) ->
            let value_0 = value_of_expression expression_0 pre in
            let value_1 = value_of_expression expression_1 pre in
            let value = match value_0, value_1 with
                | None, _
                | _, None -> None
                | Some integer_0, Some integer_1 -> interpret_condition condition integer_0 integer_1 in
            let post = Ir.RegMap.add register value pre in
            post
        | I_LoadVar (register, value)
        | I_LoadStack (register, value) ->
            let post = Ir.RegMap.add register None pre in
            post
        | I_Use (registers)
        | I_Def (registers) ->
            let post = List.fold_left add_used_registers pre registers in
            post
        | _ ->
            let post = pre in
            post

    let get_instructions_knowledges label pre_registers_map =
        let rec aux knowledge = function
            | [] -> []
            | instruction :: instructions_list ->
                let post = transfer_instruction instruction knowledge in
                Analysis.Knowledge.make ~pre:knowledge ~post :: aux post instructions_list in
        aux pre_registers_map (ControlFlowGraph.block cfg label)

    let get_post pre = function
        | [] -> pre
        | instructions_knowledges -> Analysis.Knowledge.post (List.nth instructions_knowledges (List.length instructions_knowledges - 1))

    let get_body instructions_knowledges label =
        List.combine instructions_knowledges (ControlFlowGraph.block cfg label)

    let get_terminator registers_map label =
        Analysis.Knowledge.make ~pre:registers_map ~post:registers_map, ControlFlowGraph.terminator cfg label

    let compute_knowledge label =
        (* entry -> parameters are top
           else -> (in = sum(predecessors); out = transfer(in)) for all instructions *)
        if label == ControlFlowGraph.entry_label cfg then Analysis.(BlockKnowledge.make_simple (Knowledge.make ~pre:initial ~post:initial))
        else if label <> ControlFlowGraph.exit_label cfg then
            let pre = List.fold_left sum_knowledge Ir.RegMap.empty (List.map (Hashtbl.find_opt result) (ControlFlowGraph.predecessors cfg label)) in
            let instructions_knowledges = get_instructions_knowledges label pre in
            let post = get_post pre instructions_knowledges in
            let block = Analysis.Knowledge.make ~pre ~post in
            let body = get_body instructions_knowledges label in
            let terminator = get_terminator post label in
            Analysis.BlockKnowledge.make_complex ~block ~body ~terminator
        else Analysis.(BlockKnowledge.make_simple (Knowledge.make ~pre:initial ~post:initial))

    let rec unique_concatenation list_0 = function
        | [] -> list_0
        | element :: list_1 ->
            if List.mem element list_0 then unique_concatenation list_0 list_1
            else unique_concatenation (element :: list_0) list_1

    let equal_knowledges knowledge_0 knowledge_1 =
        (* let aux binding_0 binding_1 = match binding_0, binding_1 with
            | None, None -> true
            | Some value_0, Some value_1 -> value_0 == value_1
            | _ -> false in
        Ir.RegMap.equal aux (Analysis.Knowledge.pre knowledge_0) (Analysis.Knowledge.pre knowledge_1) &&
        Ir.RegMap.equal aux (Analysis.Knowledge.post knowledge_0) (Analysis.Knowledge.post knowledge_1) *)
        let aux knowledge_0 register binding result =
            if not result then result
            else match binding, Ir.RegMap.find register knowledge_0 with
                | None, None -> true
                | Some value_0, Some value_1 -> value_0 == value_1
                | _ -> false in
        Ir.RegMap.fold (aux (Analysis.Knowledge.pre knowledge_0)) (Analysis.Knowledge.pre knowledge_1) true &&
        Ir.RegMap.fold (aux (Analysis.Knowledge.post knowledge_0)) (Analysis.Knowledge.post knowledge_1) true

    let rec equal_bodies body0 body1 = match body0, body1 with
        | [], [] -> true
        | (knowledge0, instruction0) :: body0, (knowledge1, instruction1) :: body1 ->
            equal_knowledges knowledge0 knowledge1 && equal_bodies body0 body1
        | _ -> failwith "Not-equal-length-bodies compared; I don't care about this case; this function should be used for same-length bodies"

    let equal_terminators (knowledge0, terminator0) (knowledge1, terminator1) = equal_knowledges knowledge0 knowledge1

    let equal_complex_block_knowledges complex0 complex1 =
        equal_knowledges (Analysis.BlockKnowledge.block complex0) (Analysis.BlockKnowledge.block complex1) &&
        equal_bodies (Analysis.BlockKnowledge.body complex0) (Analysis.BlockKnowledge.body complex1) &&
        equal_terminators (Analysis.BlockKnowledge.terminator complex0) (Analysis.BlockKnowledge.terminator complex1)

    let equal_block_knowledges block_knowledge0 block_knowledge1 = match block_knowledge0, block_knowledge1 with
        | Analysis.BlockKnowledge.Simple knowledge0, Analysis.BlockKnowledge.Simple knowledge1 -> equal_knowledges knowledge0 knowledge1
        | (Analysis.BlockKnowledge.Complex _ as complex0), (Analysis.BlockKnowledge.Complex _ as complex1) -> equal_complex_block_knowledges complex0 complex1
        | _ -> false

    let analyse () =
        (* start with entry block
           analyse a block and add its successors to the queue
           return if queue is empty *)
        let rec aux = function
            | [] -> ()
            | label :: labels_list ->
                let knowledge = compute_knowledge label in
                match Hashtbl.find_opt result label with
                | None ->
                    Hashtbl.replace result label knowledge;
                    aux (unique_concatenation labels_list (ControlFlowGraph.successors cfg label))
                | Some old_knowledge ->
                    if equal_block_knowledges knowledge old_knowledge then aux labels_list
                    else
                        Hashtbl.replace result label knowledge;
                        aux (unique_concatenation labels_list (ControlFlowGraph.successors cfg label)) in
        aux [ControlFlowGraph.entry_label cfg];
        result
  end



  (* Skontruuj wartość ekstremalną *)
  let make_initial n =
    (* n first temporary registers *)
    let rec aux result i =
        if i == n then result
        else aux (Ir.RegMap.add (REG_Tmp i) None result) (i + 1) in
    aux Ir.RegMap.empty 0

  let analyse proc : Xi_lib.Analysis_domain.ConstantFolding.table =
    let initial = make_initial @@ Ir.formal_parameters_of_procedure proc in
    let cfg = Ir.cfg_of_procedure proc in
    let module Instance = Implementation(struct let cfg = cfg let initial = initial end) in
    let result = Instance.analyse () in
    result

end
