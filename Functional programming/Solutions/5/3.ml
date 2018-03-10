open List

type htree = Leaf of char * int | Node of htree * int * htree

let cmp t0 t1 =
    let f0 = match t0 with
        Leaf (_, f) | Node (_, f, _) -> f
    and f1 = match t1 with
        Leaf (_, f) | Node (_, f, _) -> f in
    if f0 < f1 then -1
    else if f0 = f1 then 0
    else 1

let merge t0 t1 =
    let f0 = match t0 with
        Leaf (_, f) | Node (_, f, _) -> f
    and f1 = match t1 with
        Leaf (_, f) | Node (_, f, _) -> f in
    Node (t0, f0 + f1, t1)

let rec insert t l =
    match l with
    [] -> [t]
    | hd :: tl -> match hd with
        Leaf (_, f0) | Node (_, f0, _) -> match t with
        Leaf (_, f1) | Node (_, f1, _) -> if f0 < f1 then hd :: insert t tl
            else t :: l

let mkHTree l =
    let converted = map (fun (s, f) -> Leaf (s, f)) l in
    let sl = sort cmp converted in
    let rec aux = function
        [t] -> t
        | hd0 :: hd1 :: tl -> aux (insert (merge hd0 hd1) tl) in
    aux sl

type 'a stream = Nil | Cons of 'a * 'a stream

let find s t =
    let rec aux p = function
        Leaf (s', _) -> if s = s' then Some p else None
        | Node (l, _, r) -> let p' = p lsl 1 in
            match aux p' l with
            Some p'' -> Some p''
            | None -> aux p' r in
    match aux 0 t with
    Some p -> p

let len n =
    let rec aux e p =
        if n < p then e
        else aux (e + 1) (2 * p) in
    aux 0 1

let encode t s =
    let rec encode t p = function
        Nil -> Nil
        | Cons (c, s) -> let p' = find c t in
            let l = len p and l' = len p' in
            if l + l' < 8 then encode t ((p lsl l') + p') s
            else let empty = 8 - l in
                let p'' = p' lsr (l' - empty) in
                let byte = (p lsl empty) + p'' in
                Cons (Char.chr byte, encode t (p' - (p'' lsl (l' - empty))) s) in
    encode t 0 s

let lookup p t =
    let l = len p in
    let rec aux sh = function
        Leaf (s, _) -> Some s
        | Node (l, _, r) -> if sh = 0 then None
            else if (p lsr sh) land 1 = 0 then aux (sh - 1) l
            else aux (sh - 1) r in
    aux (l - 1)

let decode t s =
    let rec decode t p = function
        Nil -> Nil
        | Cons (c, s) -> Nil (* TODO *) in
    None
