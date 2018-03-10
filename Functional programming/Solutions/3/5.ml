open List

let rec take n l =
    if n = 0 then []
    else match l with
    hd :: tl -> hd :: take (n - 1) tl

let rec drop n l =
    if n = 0 then l
    else match l with
    hd :: tl -> drop (n - 1) tl

let rec take_while cond l =
    match l with
    [] -> []
    | hd :: tl -> if cond hd then hd :: take_while cond tl else []

let next_perm p =
    let rec rev_suffix p acc =
        match p with
        [x] -> x :: acc
        | hd0 :: hd1 :: tl ->
            if hd0 >= hd1 then rev_suffix (hd1 :: tl) (hd0 :: acc)
            else rev_suffix (hd1 :: tl) [] in
    let len = length p in
    let rev_suf = rev_suffix p [] in
    let suf_len = length rev_suf in
    if suf_len = len then rev_suf
    else let pref_no_pivot = take (len - suf_len - 1) p in
        let pivot = nth p (len - suf_len - 1) in
        let suf_init = take_while ((>) pivot) rev_suf in
        let new_pivot :: suf_tail = drop (length suf_init) rev_suf in
        let new_suf = suf_init @ (pivot :: suf_tail) in
        pref_no_pivot @ (new_pivot :: new_suf)
