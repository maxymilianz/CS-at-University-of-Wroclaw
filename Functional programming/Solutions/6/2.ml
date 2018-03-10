open List

type 'a btree = Leaf of 'a | Node of 'a btree * 'a * 'a btree

let enumerate_preord t =
    let rec aux n = function
        Leaf _ -> (Leaf n, n + 1)
        | Node (l, _, r) -> let l_done = aux (n + 1) l in match l_done with
            t, m -> let r_done = aux m r in match r_done with
                t', m' -> (Node (t, n, t'), m') in
    fst (aux 1 t)

(* let rec concat l0 l1 =
    match l0, l1 with
    [], l | l, [] -> l
    | hd0 :: tl0, hd1 :: tl1 -> (hd0 @ hd1) :: concat tl0 tl1

let indexes l =
    let rec aux n = function
        [] -> []
        | hd :: tl -> n :: aux (n + length hd) tl in
    aux 1 l

let rec to_lists = function
    Leaf v -> [[v]]
    | Node (l, v, r) -> [v] :: concat (to_lists l) (to_lists r) *)

let count t =
    let rec aux t lst =
        match t with
        Leaf _ -> (match lst with
            [] -> [1]
            | hd :: tl -> hd + 1 :: tl)
        | Node (l, _, r) -> match lst with
            [] -> let ll = aux l [] in
                let rl = aux r ll in
                1 :: rl
            | hd :: tl -> let ll = aux l tl in
                let rl = aux r ll in
                hd + 1 :: rl in
    aux t []

let indexes' l =
    let rec aux n = function
        [] -> []
        | hd :: tl -> n :: aux (n + hd) tl in
    aux 1 l

let enumerate_breadth t =
    let rec aux (hd :: tl) = function
        Leaf _ -> (Leaf hd, hd + 1 :: tl)
        | Node (l, _, r) -> let (l_done, new_tl) = aux tl l in
            let (r_done, new_tl') = aux new_tl r in
            (Node (l_done, hd, r_done), hd + 1 :: new_tl') in
    fst (aux (indexes' (count t)) t)
