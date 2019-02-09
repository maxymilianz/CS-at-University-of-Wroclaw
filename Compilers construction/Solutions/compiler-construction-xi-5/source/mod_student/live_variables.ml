open Xi_lib
open Iface
open Ir
open Ir_utils
open Analysis (* <--- tu mogą być pomocne komentarze *)
open Analysis_domain

module Make() = struct

    module Implementation(M:sig val cfg: ControlFlowGraph.t end) = struct
        open M

        (*
         * Zwróćmy tablicę gdzie każdy wierzchołek jest zainicjalizowany na
         * konstruktor Simple (typ BlockKnowledge) gdzie na wejściu/wyjściu
         * bloku mamy pusty zbiór rejestrów.
         *
         * Wierzchołki oznaczające basic-bloki powinny ostatecznie być opisane
         * konstruktorem Complex, ale początkowo dla wygody możemy ustawić je na Simple.
         * Ważne aby funkcja przeliczająca wiedzę dla bloku podstawowego ostatecznie
         * opisał blok za pomocą konstruktora Complex.
         *)
        let initialize_table () =
            let table = Hashtbl.create 513 in
            let kw = Knowledge.make ~pre:RegSet.empty ~post:RegSet.empty in
            let blk_kw = BlockKnowledge.make_simple kw in
            let set v =
                Hashtbl.replace table v blk_kw
            in
            List.iter set @@ ControlFlowGraph.labels cfg;
            table


        let result : LiveVariables.table = initialize_table ()

        let transfer_instruction instruction post =
            let kill = RegSet.of_list (defined_registers_instr instruction) in
            let gen = RegSet.of_list (used_registers_instr instruction) in
            let pre = RegSet.union (RegSet.diff post kill) gen in
            Knowledge.make ~pre ~post

        let transfer_terminator terminator post =
            let kill = RegSet.of_list (defined_registers_terminator terminator) in
            let gen = RegSet.of_list (used_registers_terminator terminator) in
            let pre = RegSet.union (RegSet.diff post kill) gen in
            Knowledge.make ~pre ~post

        let get_instructions_knowledges label post_registers_set =
            let rec aux knowledge = function
                | [] -> [knowledge]
                | instruction :: instructions_list ->
                    let next_knowledges = aux knowledge instructions_list in
                    transfer_instruction instruction (Knowledge.pre (List.hd next_knowledges)) :: next_knowledges in
            let terminator_knowledge = transfer_terminator (ControlFlowGraph.terminator cfg label) post_registers_set in
            aux terminator_knowledge (ControlFlowGraph.block cfg label)

        let sum_knowledge registers_set block_knowledge = RegSet.union registers_set (BlockKnowledge.pre block_knowledge)

        let update_entry label =
            let post = List.fold_left sum_knowledge RegSet.empty (List.map (Hashtbl.find result) (ControlFlowGraph.successors cfg label)) in
            let pre = post in
            let knowledge = Knowledge.make ~pre ~post in
            let block_knowledge = BlockKnowledge.make_simple knowledge in
            Hashtbl.replace result label block_knowledge

        let get_body instructions_knowledges label =
            let rec aux knowledges_list instructions_list =
                match knowledges_list, instructions_list with
                | [terminator_knowledge], [] -> []
                | knowledge :: knowledges_list, instruction :: instructions_list ->
                    (knowledge, instruction) :: aux knowledges_list instructions_list
                | _ -> failwith "Instructions knowledges lists length != instructions lists length + 1; this should never happen" in
            aux instructions_knowledges (ControlFlowGraph.block cfg label)

        let get_terminator instructions_knowledges label =
            let knowledge = List.nth instructions_knowledges (List.length instructions_knowledges - 1) in
            let terminator = ControlFlowGraph.terminator cfg label in
            knowledge, terminator

        let update_label label =
            if label == ControlFlowGraph.entry_label cfg then update_entry label
            else if label <> ControlFlowGraph.exit_label cfg then
                let post = List.fold_left sum_knowledge RegSet.empty (List.map (Hashtbl.find result) (ControlFlowGraph.successors cfg label)) in
                let instructions_knowledges = get_instructions_knowledges label post in
                let pre = Knowledge.pre (List.hd instructions_knowledges) in
                let block = Knowledge.make ~pre ~post in
                let body = get_body instructions_knowledges label in
                let terminator = get_terminator instructions_knowledges label in
                let block_knowledge = BlockKnowledge.make_complex ~block ~body ~terminator in
                Hashtbl.replace result label block_knowledge

        let update_result () =
            List.iter update_label (ControlFlowGraph.labels cfg)

        let equal_knowledges knowledge0 knowledge1 =
            RegSet.equal (Knowledge.pre knowledge0) (Knowledge.pre knowledge1) &&
            RegSet.equal (Knowledge.post knowledge0) (Knowledge.post knowledge1)

        let rec equal_bodies body0 body1 = match body0, body1 with
            | [], [] -> true
            | (knowledge0, instruction0) :: body0, (knowledge1, instruction1) :: body1 ->
                equal_knowledges knowledge0 knowledge1 && equal_bodies body0 body1
            | _ -> failwith "Not-equal-length-bodies compared; I don't care about this case; this function should be used for same-length bodies"

        let equal_terminators (knowledge0, terminator0) (knowledge1, terminator1) = equal_knowledges knowledge0 knowledge1

        let equal_complex_block_knowledges complex0 complex1 =
            equal_knowledges (BlockKnowledge.block complex0) (BlockKnowledge.block complex1) &&
            equal_bodies (BlockKnowledge.body complex0) (BlockKnowledge.body complex1) &&
            equal_terminators (BlockKnowledge.terminator complex0) (BlockKnowledge.terminator complex1)

        let equal_block_knowledges block_knowledge0 block_knowledge1 = match block_knowledge0, block_knowledge1 with
            | BlockKnowledge.Simple knowledge0, BlockKnowledge.Simple knowledge1 -> equal_knowledges knowledge0 knowledge1
            | (BlockKnowledge.Complex _ as complex0), (BlockKnowledge.Complex _ as complex1) -> equal_complex_block_knowledges complex0 complex1
            | _ -> false

        let equal_hashtables hashtable0 hashtable1 =
            let rec aux key1 value1 = function
                | false -> false
                | true -> match Hashtbl.find_opt hashtable0 key1 with
                    | None -> false
                    | Some value0 -> equal_block_knowledges value0 value1 in
            Hashtbl.fold aux hashtable1 true

        let rec compute_fixpoint () =
            (* copy current result to result';
               update all labels values in result;
               repeat if result != result' *)
            let old_result = Hashtbl.copy result in
            update_result ();
            if equal_hashtables old_result result then ()
            else compute_fixpoint ()

        let analyse () =
            compute_fixpoint ();
            result

    end

    let analyse cfg =
        let module Instance = Implementation(struct let cfg = cfg end) in
        Instance.analyse ()


end
