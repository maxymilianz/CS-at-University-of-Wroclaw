open Xi_lib.Iface
open Xi_lib.Plugin
open Xi_lib.Plugin_register


module LexerAndParser = struct

  type token = Parser.token

  module Lexer = Lexer

  module Parser = Parser

end

module Plugin : PLUGIN = struct

  let version = "na"

  let make_live_variables_analysis = None

  let make_dominators_analysis = None

  let make_scheduler = None

  let make_natural_loops_analysis = None

  let make_spill_costs_analysis = None

  let lexer_and_parser = None
  (*
   * Przenieś pliki parser.mly oraz lexer.mll z poprzedniego rozwiązania 
   * i odkomentuj poniższą linijkę.
   *
   * Przenoszenie rozwiązania nie jest wymagane. Pamiętaj, że możesz napotkać
   * trudności gdy rozwiązanie z poprzedniej pracowni okaże się nie do końca
   * kompatybilne z kształtem danych oczekiwanym przez resztę modułów
   * kompilatora.
   *
  let lexer_and_parser = Some (module LexerAndParser : LEXER_AND_PARSER)
   *)

  let make_typechecker = Some (module Typechecker.Make : MAKE_TYPECHECKER)

  let make_translator = None

  let make_jump_threading = None

  let make_constant_folding = None

  let make_hilower = None

  let make_callconv = None

  let make_mipslower = None

  let make_register_allocator = None

  let make_constant_folding_analysis = None

  let make_codegen = None

  let make_dead_code_elimination = None

  let make_interference_graph_analysis = None

  let make_spilling = None

  let make_reachability_analysis = None
end

module RegisterMyPlugin = RegisterPlugin(Plugin)
