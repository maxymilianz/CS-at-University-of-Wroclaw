{
    open Xi_lib
    open Parser
    open Parser_utils

    (* Lexing z biblioteki standardowej ocamla *)
    open Lexing

    (* Standardowo w YACC-podobnych narzędziach  to lekser jest uzależniony od parsera. To znaczy, że typ
     * danych z tokenami definiuje moduł wygenerowany na bazie grammar.mly. Definiujemy alias na typ
     * tokenu na potrzeby interfejsów Xi_lib.Iface *)
    type token = Parser.token

    (* Obsługa błędu *)
    let handleError pos token =
        let exc = InvalidToken (mkLocation pos, token) in
        raise exc

    (* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
     * Miejsce na twój kod w Ocamlu
     *)

    exception WrongChar

    (* https://stackoverflow.com/questions/10191093/escape-sequences-in-ocaml *)

    let string_to_char text =
        (* let unescaped = Scanf.unescaped text in
        if String.length unescaped == 3 then unescaped.[1]
        else raise WrongChar *)
        (* text.[1] *)
        if String.length text == 3 then text.[1]
        else match text.[2] with
            | '\'' -> '\''
            | '\\' -> '\\'
            | 'n' -> '\n'
            | _ -> raise WrongChar

    let string_to_string text =
        let length = String.length text - 1 in
        let rec aux index result =
            if index >= length then result
            else Char.escaped text.[index] ^ (aux (index + 1) result) in
        aux 1 ""

    (* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       ----------------------------------------------------------------------------- *)

}

(* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
 * Miejsce na nazwane wyrażenia regularne
 *)

let whitespace = ' ' | '\t'

let leftParenthesis = '('
let rightParenthesis = ')'

let leftBrace = '{'
let rightBrace = '}'

let leftBracket = '['
let rightBracket = ']'

let comma = ','

let colon = ':'

let semicolon = ';'

let assign = '='

let equal = "=="
let unequal = "!="
let less = '<'
let lessEqual = "<="
let greater = '>'
let greaterEqual = ">="

let plus = '+'
let minus = '-'
let times = '*'
let divide = '/'
let modulo = '%'
let andOperator = '&'
let orOperator = '|'

let notOperator = '!'
(* let negate = '-' *)      (* to samo co minus *)

let length = "length"

let returnKeyword = "return"
let whileKeyword = "while"
let ifKeyword = "if"
let elseKeyword = "else"

let underscore = '_'

let boolValue = "true" | "false"

let charValue = '\'' ([^ '\\' '\''] | ('\\' ['\\' '\"' '\'' 'n'])) '\''

let digit = ['0'-'9']
let intValue = digit+

let stringValue = '"' ([^ '\\' '"' '\n' '\t']* ('\\' [^ '\n' '\t'])?)+ '"'

let intTypename = "int"
let boolTypename = "bool"

let identifier = ['a'-'z' '_' 'A'-'Z']['_' 'A'-'Z' 'a'-'z' '0'-'9']*

(* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ----------------------------------------------------------------------------- *)


rule token = parse
    (* Trzeba pamiętać aby uaktualnić pozycje w lexbuf, gdy widzimy znak końca wiersza.
     * To się samo nie robi. Moduł Lexing z standardowej biblioteki daje do tego wygodną
     * funkcję new_line.
     *)
    | ['\n'] { new_line lexbuf; token lexbuf }

    (* widzimy początek komentarza i przechodzimy do pomocniczego stanu *)
    | "//" { line_comment lexbuf }

    | eof { EOF }

    (* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
     * Miejsce na twoje reguły
     *)

    | whitespace { token lexbuf }

    | leftParenthesis { LEFT_PARENTHESIS }
    | rightParenthesis { RIGHT_PARENTHESIS }

    | leftBrace { LEFT_BRACE }
    | rightBrace { RIGHT_BRACE }

    | leftBracket { LEFT_BRACKET }
    | rightBracket { RIGHT_BRACKET }

    | comma { COMMA }

    | colon { COLON }

    | semicolon { SEMICOLON }

    | assign { ASSIGN }

    | equal { EQUAL }
    | unequal { UNEQUAL }
    | less { LESS }
    | lessEqual { LESS_EQUAL }
    | greater { GREATER }
    | greaterEqual { GREATER_EQUAL }

    | plus { PLUS }
    | minus { MINUS }
    | times { TIMES }
    | divide { DIVIDE }
    | modulo { MODULO }
    | andOperator { AND }
    | orOperator { OR }

    | notOperator { NOT }
    (* | negate { NEGATE } *)

    | length { LENGTH }

    | returnKeyword { RETURN_KEYWORD }
    | whileKeyword { WHILE_KEYWORD }
    | ifKeyword { IF_KEYWORD }
    | elseKeyword { ELSE_KEYWORD }

    | underscore { UNDERSCORE }

    | boolValue as boolean { BOOL(bool_of_string boolean) }
    | charValue as text { CHAR(string_to_char text) }
    | intValue as integer { INT(Int32.of_int (int_of_string integer)) }
    | stringValue as text { STRING(string_to_string text) }

    | intTypename { INT_TYPENAME }
    | boolTypename { BOOL_TYPENAME }

    | identifier as id { IDENTIFIER(id) }

    (* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       ----------------------------------------------------------------------------- *)

    | _ { handleError (Lexing.lexeme_start_p lexbuf) (Lexing.lexeme lexbuf) }

(* Pomocniczy stan aby wygodnie i prawidłowo obsłużyć komentarze *)
and line_comment = parse
    | '\n' { new_line lexbuf; token lexbuf }

    (* Niektóre edytory nie wstawiają znaku końca wiersza w ostatniej linijce, jesteśmy
     * przygotowani na obsługę takiego komentarza.
     *)
    | eof { EOF }

    | _ { line_comment lexbuf }
