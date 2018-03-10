let nat_stream x = x;;

let hd s = s 0;;
let tl s =
    let rec loop n = loop (n + 1) in
    hd (loop 0);;

let add a s n = s n + a;;

let map f s n = f (s n);;

let map2 f s0 s1 n = f (s0 n) (s1 n);;

(* replace i take uzywaja 'i' tak, jak inne funkcje 'n' *)

let replace n a s i =
    if i mod n = 0 then a
    else s i;;

let take n s i = s (n * i);;

let rec fold f a s n =
    (* if n = 0 then f a (s n)
    else f (fold f a s (n - 1)) (s n);; *)
    f (if n = 0 then a else (fold f a s (n - 1))) (s n);;

let rec tabulate s ?(i = 0) n =
    if i = n then []
    else [s i] @ tabulate s ~i:(i + 1) n;;

let sum_stream = fold (+) 0 nat_stream;;
let prod_stream = fold ( *) 1 nat_stream;;
let a_stream n = 'a';;
let neg_stream n = -n;;
let check_if_prime_stream n =
    let rec check_if_prime n i =
        if n >= 2 then
            if i >= 2 && n mod i <> 0 then check_if_prime n (i - 1)
            else i < 2
        else false in
    check_if_prime n (n - 1);;
