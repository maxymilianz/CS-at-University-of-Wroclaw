(*
 * Menhir wygeneruje funkcję o nazwie file
 *)
%start <Xi_lib.Ast.module_definition> file

%{
open Xi_lib
open Ast
open Parser_utils

(* Generator znaczników *)
let mkTag =
    let i = ref 0 in
    fun () ->
        let tag = !i in
        incr i;
        NodeTag tag

exception WrongArrayDimensions
exception WrongLvalue

(* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
 * Miejsce na twój kod w Ocamlu
 *)

(* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ----------------------------------------------------------------------------- *)

%}

(* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
 * Miejsce na dyrektywy
 *)

%token LEFT_PARENTHESIS
%token RIGHT_PARENTHESIS

%token LEFT_BRACE
%token RIGHT_BRACE

%token LEFT_BRACKET
%token RIGHT_BRACKET

%token COMMA

%token COLON

%token SEMICOLON

%token ASSIGN

%token EQUAL
%token UNEQUAL
%token LESS
%token LESS_EQUAL
%token GREATER
%token GREATER_EQUAL

%token PLUS
%token MINUS
%token TIMES
%token DIVIDE
%token MODULO
%token AND
%token OR

%token NOT
(* %token NEGATE *) (* to samo co MINUS *)

%token LENGTH

%token RETURN_KEYWORD
%token WHILE_KEYWORD
%token IF_KEYWORD
%token ELSE_KEYWORD

%token UNDERSCORE

%token <bool> BOOL
%token <char> CHAR
%token <int32> INT
%token <string> STRING

%token INT_TYPENAME
%token BOOL_TYPENAME

%token EOF
%token <string> IDENTIFIER

%left OR
%left AND
%left EQUAL UNEQUAL
%left LESS LESS_EQUAL GREATER GREATER_EQUAL
%left PLUS MINUS
%left TIMES DIVIDE MODULO
%nonassoc UNARY_OPERATOR

(* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ----------------------------------------------------------------------------- *)

%%

(* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
 * Miejsce na gramatykę
 *)


(* Obecnie potrafimy sparsować tylko pusty plik (wymagamy od razu tokena EOF) *)
file:
    (* | EOF { ModuleDefinition { global_declarations=[] } } *)
    | global_declarations_list { ModuleDefinition { global_declarations = $1 } }

global_declarations_list:
    | EOF { [] }
    | global_declaration; global_declarations_list { $1 :: $2 }

global_declaration:
    | identifier; LEFT_PARENTHESIS; formal_parameters_list; RIGHT_PARENTHESIS; return_types_list; maybe_body
        { GDECL_Function { loc = mkLocation $startpos; id = $1; formal_parameters = $3; return_types = $5; body = $6 } }

identifier:
    | IDENTIFIER { Identifier $1 }

formal_parameters_list:
    | (* empty *) { [] }
    | nonempty_formal_parameters_list { $1 }

nonempty_formal_parameters_list:
    | variable_declaration { [$1] }
    | variable_declaration; COMMA; nonempty_formal_parameters_list { $1 :: $3 }

variable_declaration:
    | identifier; COLON; type_expression
        { VarDecl { loc = mkLocation $startpos; id = $1; tp = $3 } }

return_types_list:
    | (* empty *) { [] }
    | COLON; nonempty_return_types_list { $2 }

nonempty_return_types_list:
    | type_expression { [$1] }
    | type_expression; COMMA; nonempty_return_types_list { $1 :: $3 }

type_expression:
    | basic_type_expression { $1 }
    | basic_type_expression; array_dimensions
        { let rec aux t dimensions = match dimensions with
                | [hd] -> TEXPR_Array { loc = mkLocation $startpos; sub = t; dim = hd }
                | hd :: tl -> TEXPR_Array { loc = mkLocation $startpos; sub = aux t tl; dim = hd }
                | _ -> raise WrongArrayDimensions
            in aux $1 (List.rev $2) }

basic_type_expression:
    | INT_TYPENAME { TEXPR_Int { loc = mkLocation $startpos } }
    | BOOL_TYPENAME { TEXPR_Bool { loc = mkLocation $startpos } }

array_dimensions:
    | (* empty *) { [] }
    | LEFT_BRACKET; RIGHT_BRACKET; array_dimensions { None :: $3 }
    | LEFT_BRACKET; expression; RIGHT_BRACKET; array_dimensions { Some $2 :: $4 }

maybe_body:
    | (* empty *) { None }
    | body { Some $1 }

body:
    | LEFT_BRACE; statements_list; maybe_return; maybe_semicolon; RIGHT_BRACE
        { STMTBlock { loc = mkLocation $startpos; body = $2 @ $3 } }

maybe_return:
    | (* empty *) { [] }
    | return_statement { [$1] }

statements_list:
    | (* empty *) { [] }
    | statement; maybe_semicolon; statements_list { $1 :: $3 }

maybe_semicolon:
    | (* empty *) { }
    | SEMICOLON { }

statement:
    | call { STMT_Call $1 }
    | assign { $1 }
    | variable_declaration_statement { $1 }
    | if_statement { $1 }
    | while_statement { $1 }
    | multiple_variables_declaration { $1 }
    | body { STMT_Block $1 }

call:
    | identifier; LEFT_PARENTHESIS; expressions_list; RIGHT_PARENTHESIS
        { Call { tag = mkTag (); loc = mkLocation $startpos; callee = $1; arguments = $3 } }

expressions_list:
    | (* empty *) { [] }
    | nonempty_expressions_list { $1 }

nonempty_expressions_list:
    | expression { [$1] }
    | expression; COMMA; nonempty_expressions_list { $1 :: $3 }

expression:
    | identifier_expression { $1 }
    | int_expression { $1 }
    | char_expression { $1 }
    | string_expression { $1 }
    | bool_expression { $1 }
    | relation { $1 }
    | binary_expression { $1 }
    | length { $1 }
    | unary_expression { $1 }
    | call { EXPR_Call $1 }
    | index_expression { $1 }
    | structure { $1 }

identifier_expression:
    | identifier
        { EXPR_Id { tag = mkTag (); loc = mkLocation $startpos; id = $1 } }

int_expression:
    | INT { EXPR_Int { tag = mkTag (); loc = mkLocation $startpos; value = $1 } }

char_expression:
    | CHAR { EXPR_Char { tag = mkTag (); loc = mkLocation $startpos; value = $1 } }

string_expression:
    | STRING { EXPR_String { tag = mkTag (); loc = mkLocation $startpos; value = $1 } }

bool_expression:
    | BOOL { EXPR_Bool { tag = mkTag (); loc = mkLocation $startpos; value = $1 } }

relation:
    | expression; relation_operator; expression
        { EXPR_Relation { tag = mkTag (); loc = mkLocation $startpos; op = $2; lhs = $1; rhs = $3 } }

%inline relation_operator:
    | EQUAL { RELOP_Eq }
    | UNEQUAL { RELOP_Ne }
    | LESS { RELOP_Lt }
    | GREATER { RELOP_Gt }
    | LESS_EQUAL { RELOP_Le }
    | GREATER_EQUAL { RELOP_Ge }

binary_expression:
    | expression; binary_operator; expression
        { EXPR_Binop { tag = mkTag (); loc = mkLocation $startpos; op = $2; lhs = $1; rhs = $3 } }

%inline binary_operator:
    | AND { BINOP_And }
    | OR { BINOP_Or }
    | PLUS { BINOP_Add }
    | MINUS { BINOP_Sub }
    | TIMES { BINOP_Mult }
    | DIVIDE { BINOP_Div }
    | MODULO { BINOP_Rem }

length:
    | LENGTH; LEFT_PARENTHESIS; expression; RIGHT_PARENTHESIS
        { EXPR_Length { tag = mkTag (); loc = mkLocation $startpos; arg = $3 } }

unary_expression:
    | unary_operator; expression %prec UNARY_OPERATOR
        { EXPR_Unop { tag = mkTag (); loc = mkLocation $startpos; op = $1; sub = $2 } }

unary_operator:
    | NOT { UNOP_Not }
    | MINUS { UNOP_Neg }

index_expression:
    | expression; LEFT_BRACKET; expression; RIGHT_BRACKET
        { EXPR_Index { tag = mkTag (); loc = mkLocation $startpos; expr = $1; index = $3 } }

structure:
    | LEFT_BRACE; expressions_list; maybe_comma; RIGHT_BRACE
        { EXPR_Struct { tag = mkTag (); loc = mkLocation $startpos; elements = $2 } }

maybe_comma:
    | (* empty *) { }
    | COMMA { }

assign:
    | lvalue; ASSIGN; expression
        { STMT_Assign { loc = mkLocation $startpos; lhs = $1; rhs = $3 } }

lvalue:
    | identifier { LVALUE_Id { loc = mkLocation $startpos; id = $1 } }
    | structure { raise WrongLvalue }       (* no need to check what is after structure *)
    | expression; LEFT_BRACKET; expression; RIGHT_BRACKET
        { LVALUE_Index { loc = mkLocation $startpos; sub = $1; index = $3 } }

variable_declaration_statement:
    | variable_declaration; maybe_variable_initializer
        { STMT_VarDecl { var = $1; init = $2 } }

maybe_variable_initializer:
    | (* empty *) { None }
    | ASSIGN; expression { Some $2 }

if_statement:
    | IF_KEYWORD; maybe_parenthesesed_expression; statement; else_statement
        { STMT_If { loc = mkLocation $startpos; cond = $2; then_branch = $3; else_branch = $4 } }

maybe_parenthesesed_expression:
    | expression { $1 }
    | LEFT_PARENTHESIS; expression; RIGHT_PARENTHESIS { $2 }

else_statement:
    | (* empty *) { None }
    | ELSE_KEYWORD; statement { Some $2 }

while_statement:
    | WHILE_KEYWORD; maybe_parenthesesed_expression; statement
        { STMT_While { loc = mkLocation $startpos; cond = $2; body = $3 } }

return_statement:
    | RETURN_KEYWORD; expressions_list
        { STMT_Return { loc = mkLocation $startpos; values = $2 } }

multiple_variables_declaration:
    | maybe_variable_declaration; COMMA; maybe_variable_declarations_list; ASSIGN; call
        { STMT_MultiVarDecl { loc = mkLocation $startpos; vars = $1 :: $3; init = $5 } }

maybe_variable_declarations_list:
    | maybe_variable_declaration { [$1] }
    | maybe_variable_declaration; COMMA; maybe_variable_declarations_list { $1 :: $3 }

maybe_variable_declaration:
    | UNDERSCORE { None }
    | variable_declaration { Some $1 }

(*
   ** przykład użycia mkLocation

    use_declaration:
        | USE suffix(identifier, opt(SEMICOLON))
        { GDECL_Use {loc=mkLocation $startpos; id=$2} }

   ** przykład użycia mkTag

    atomic_expression:
        | identifier
        { EXPR_Id {loc=mkLocation $startpos; id=$1; tag=mkTag ()} }
*)

(* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ----------------------------------------------------------------------------- *)
