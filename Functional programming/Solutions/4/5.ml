type 'a btree = Leaf | Node of 'a btree * 'a * 'a btree

let rec prod = function
    Leaf -> 1
    | Node (l, v, r) -> v * prod l * prod r

let rec prod_cps t c =
    match t with
    Leaf -> c 1
    | Node (l, v, r) -> if v = 0 then 0
        else prod_cps l (fun vl -> prod_cps r (fun vr -> c (vl * v * vr)))

let prod_cps' t c =
    let rec aux queue c =
        match queue with
        [] -> c 1
        | Leaf :: tl -> aux tl (fun x -> c x)
        | Node (l, v, r) :: tl -> aux (l :: r :: tl) (fun x -> c (v * x)) in
    aux [t] (fun x -> x)

exception Zero

let rec prod_cps_e t c =
    match t with
    Leaf -> c 1
    | Node (l, v, r) ->
        if v = 0 then raise Zero
        else prod_cps l (fun x -> c (v * x * prod_cps r (fun x -> x)))

let prod_cps_e' t c =
    let rec aux queue c =
        match queue with
        [] -> c 1
        | Leaf :: tl -> aux tl (fun x -> c x)
        | Node (l, v, r) :: tl ->
            if v = 0 then raise Zero
            else aux (l :: r :: tl) (fun x -> c (v * x)) in
    try aux [t] (fun x -> x) with Zero -> 0
