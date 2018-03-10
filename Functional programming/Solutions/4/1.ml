let palindrome l =
    let rec aux l0 l1 =
        match (l0, l1) with
        hd :: tl, [x] -> (hd = x, tl)
        | _, hd1 :: tl1 -> let (pal, hd :: tl) = aux l0 tl1 in
            (pal && hd1 = hd, tl) in
    match l with
    [] -> true
    | _ -> fst (aux l l)
