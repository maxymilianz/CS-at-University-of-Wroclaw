open List

let halve l =
    let half_len = length l / 2 in
    let rec aux l n i =
        if n = i then ([], l)
        else match l with
            hd :: tl -> let ret = aux tl n (i + 1) in
                (hd :: fst ret, snd ret) in
    aux l half_len 0

type 'a btree = Leaf | Node of 'a btree * 'a * 'a btree

let balanced tree =
    let rec aux tree =
        match tree with
        Leaf -> (0, true)
        | Node (l, v, r) -> let ret_l = aux l and ret_r = aux r in
            (1 + (fst ret_l) + (fst ret_r),
                abs(fst ret_l - fst ret_r) <= 1 && snd ret_l && snd ret_r) in
    snd (aux tree)

let rec create l =
    match l with
    [] -> Leaf
    | hd :: tl -> let halves = halve tl in
        Node ((create (fst halves)), hd, (create (snd halves)))
