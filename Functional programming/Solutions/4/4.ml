open List

type formula =
    Var of string
    | Not of formula
    | And of formula * formula
    | Or of formula * formula

let rec del_dupl = function
    [] -> []
    | hd :: tl -> hd :: del_dupl (filter ((!=) hd) tl)

let rec vars = function
    Var s -> [s]
    | Not f -> vars f
    | And (f0, f1) -> vars f0 @ vars f1
    | Or (f0, f1) -> vars f0 @ vars f1

let rec lookup s (hd :: tl) =
    match hd with
    (s, v) -> v
    | _ -> lookup s tl

let rec compute values = function
    Var s -> lookup s values
    | Not f -> not (compute values f)
    | And (f0, f1) -> compute values f0 && compute values f1
    | Or (f0, f1) -> compute values f0 || compute values f1

let rec compute_all f = function
    [] -> (true, None)
    | v :: tl -> if compute v f = true then compute_all f tl
        else (false, Some v)

let rec nr_to_values vars nr =
    match vars with
    [] -> []
    | s :: tl -> (s, nr land 1 = 1) :: nr_to_values tl (nr lsr 1)

let numbers n =
    let last = int_of_float (2. ** n) - 1 in
    let rec aux i =
        if i = 0 then [0]
        else i :: aux (i - 1) in
    aux last

let tautology f =
    let vars = del_dupl (vars f) in
    let len = length vars in
    let numbers = numbers (float len -. 1.) in
    let all_values = map (nr_to_values vars) numbers in
    compute_all f all_values

let rec nnf = function
    Not (Not f) -> nnf f
    | Not (And (f0, f1)) -> Or (nnf (Not f0), nnf (Not f1))
    | Not (Or (f0, f1)) -> And (nnf (Not f0), nnf (Not f1))
    | And (f0, f1) -> And (nnf f0, nnf f1)
    | Or (f0, f1) -> Or (nnf f0, nnf f1)
    | literal -> literal

let rec cnf f =
    let rec dist f0 f1 =
        match (f0, f1) with
        And (f0, f1), f2 | f2, And (f0, f1) ->
            And ((dist f0 f2), (dist f1 f2))
        | f0, f1 -> Or (f0, f1) in
    let rec aux f =
        match f with
        And (f0, f1) -> And (aux f0, aux f1)
        | Or (f0, f1) -> dist (aux f0) (aux f1)
        | _ -> f in
    aux (nnf f)

let tautology' f =
    let cnff = cnf f in
    let rec vars_from_disj acc = function
        Or (f0, f1) -> vars_from_disj (vars_from_disj acc f0) f1
        | literal -> literal :: acc in
    let taut disj =
        let vars = vars_from_disj [] disj in
        let rec neg_in_l = function
            [] -> false
            | hd :: tl -> match hd with
                Var name -> mem (Not hd) tl || neg_in_l tl
                | Not var -> mem var tl || neg_in_l tl in
        neg_in_l vars in
    let rec aux = function
        And (f0, f1) -> aux f0 && aux f1
        | f -> taut f in
    aux cnff

let dnf f =
    let rec dist f0 f1 =
        match (f0, f1) with
        Or (f0, f1), f2 | f2, Or (f0, f1) ->
            Or ((dist f0 f2), (dist f1 f2))
        | f0, f1 -> And  (f0, f1) in
    let rec aux f =
        match f with
        Or (f0, f1) -> Or (aux f0, aux f1)
        | And (f0, f1) -> dist (aux f0) (aux f1)
        | _ -> f in
    aux (nnf f)

let contradictory f =
    let dnff = dnf f in
    let rec vars_from_conj acc = function
        And (f0, f1) -> vars_from_conj (vars_from_conj acc f0) f1
        | literal -> literal :: acc in
    let contr conj =
        let vars = vars_from_conj [] conj in
        let rec neg_in_l = function
            [] -> false
            | hd :: tl -> match hd with
                Var name -> mem (Not hd) tl || neg_in_l tl
                | Not var -> mem var tl || neg_in_l tl in
        neg_in_l vars in
    let rec aux = function
        Or (f0, f1) -> aux f0 && aux f1
        | f -> contr f in
    aux dnff
