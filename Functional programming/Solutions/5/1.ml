type 'a llist = LNil | LCons of 'a * (unit -> 'a llist)

let rec to_list = function
    LNil -> []
    | LCons (hd, tl) -> hd :: to_list (tl ())

let rec nth n (LCons (hd, tl)) =
    if n = 0 then hd
    else nth (n - 1) (tl ())

let rec sum n ll =
    if n = 0 then 0.
    else match ll with
        LCons (hd, tl) -> hd +. sum (n - 1) (tl ())

let sgn x = if x < 0. then -1. else 1.

let aux_pi =
    let rec aux n k = LCons (k +. 1. /. n, fun () -> aux (-.(n +. 2. *. sgn n)) (k +. 1. /. n)) in
    aux 1. 0.

let pi n = 4. *. nth n aux_pi

let rec ternary_app f (LCons (hd, tl)) =
    let tll = tl () in
    match tll with
    LCons (hd1, tl1) -> match tl1 () with
        LCons (hd2, tl2) -> match tl2 () with
            LNil -> LCons (f hd hd1 hd2, fun () -> LNil)
            | LCons (_, _) -> LCons (f hd hd1 hd2, fun () -> ternary_app f tll)

let euler x y z = z -. ((y -. z) ** 2.) /. (x -. 2. *. y +. z)

let pi_aux' = ternary_app euler aux_pi

type 'a lazy_list = LazyNil | LazyCons of 'a * 'a lazy_list Lazy.t

let rec lazy_to_list = function
    LazyNil -> []
    | LazyCons (hd, lazy tl) -> hd :: lazy_to_list tl

let rec lazy_sum n ll =
    if n = 0 then 0.
    else match ll with
        LazyCons (hd, lazy tl) -> hd +. lazy_sum (n - 1) tl

let lazy_aux_pi =
    let rec aux n = LazyCons (1. /. n, lazy (aux (-.(n +. 2. *. sgn n)))) in
    aux 1.

let lazy_pi n = 4. *. lazy_sum n lazy_aux_pi

let rec lazy_ternary_app f (LazyCons (hd, lazy tl)) =
    match tl with
    LazyCons (hd1, lazy tl1) -> match tl1 with
        LazyCons (hd2, lazy tl2) -> match tl2 with
            LazyNil -> LazyCons (f hd hd1 hd2, lazy LazyNil)
            | LazyCons (_, _) -> LazyCons (f hd hd1 hd2, lazy (lazy_ternary_app f tl))
