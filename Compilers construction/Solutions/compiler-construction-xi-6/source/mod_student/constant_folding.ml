open Xi_lib
open Ir

module Make(T:Iface.COMPILER_TOOLBOX) = struct

  module Implementation(M:sig
    val cfg : ControlFlowGraph.t
    val proc : procedure
   end) = struct

    open M

    let cfa = T.ConstantFoldingAnalysis.analyse proc

    let rewrite_instruction registers_map = function
        | I_Add (register, _, _)
        | I_Sub (register, _, _)
        | I_Div (register, _, _)
        | I_Rem (register, _, _)
        | I_Mul (register, _, _)
        | I_And (register, _, _)
        | I_Or (register, _, _)
        | I_Xor (register, _, _) as instruction ->
            (match Ir.RegMap.find register registers_map with
            | None -> instruction
            | Some value -> I_Move (register, E_Int value))
        | I_Neg (register, _)
        | I_Not (register, _)
        | I_Move (register, _) as instruction ->
            (match Ir.RegMap.find register registers_map with
            | None -> instruction
            | Some value -> I_Move (register, E_Int value))
        | I_Set (register, _, _, _) as instruction ->
            (match Ir.RegMap.find register registers_map with
            | None -> instruction
            | Some value -> I_Move (register, E_Int value))
        | instruction -> instruction

    let rec rewrite_body registers_maps block = match registers_maps, block with
        | [], [] -> []
        | (registers_map, _) :: registers_maps, instruction :: block ->
            rewrite_instruction (Analysis.Knowledge.post registers_map) instruction :: rewrite_body registers_maps block
        | _ -> failwith "Wrong number of instructions"

    let rewrite_label label =
        if label <> ControlFlowGraph.entry_label cfg && label <> ControlFlowGraph.exit_label cfg then
        ControlFlowGraph.set_block cfg label (rewrite_body (Analysis.BlockKnowledge.body (Hashtbl.find cfa label)) (ControlFlowGraph.block cfg label))
        else ()

    let rewrite () =
      Logger.extra_debug begin fun () ->
        Logger.dump_constant_folding "before-optimization" cfg cfa;
      end;
      List.iter rewrite_label (ControlFlowGraph.labels cfg)

  end


  let fold_constants proc =
    let module Instance = Implementation(struct
      let proc = proc
      let cfg = cfg_of_procedure proc
    end) in
    Instance.rewrite ()

end
