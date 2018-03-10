let rec len l =
    match l with
    [] -> 0
    | hd :: tl -> 1 + len tl

let cycle l n =
    let length = len l in
    let rec cyc_aux l i acc =
        match l with
        [] -> acc
        | hd :: tl ->
            if i >= length - n then hd :: cyc_aux tl (i + 1) acc
            else cyc_aux tl (i + 1) (hd :: acc) in
    cyc_aux l 0 []
