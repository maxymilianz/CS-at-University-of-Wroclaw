let rev l =
    let rec aux acc = function
        [] -> acc
        | hd :: tl -> aux (hd :: acc) tl in
    aux [] l

let pair_cons (e0, e1) (l0, l1) = (e0 :: l0, e1 :: l1)

let fill_tail (g, v) n =
    let rec aux (g, vhd :: vtl) n (gacc, vacc) =
        match g with
        ghd :: gtl -> if n = 0 then (rev gacc @ g, rev vacc @ ghd :: vtl)
            else aux (gtl, vtl) (n - 1) (ghd :: gacc, vhd :: vacc) in
    aux (g, v) n ([], [])

let rec fill (g, vhd :: vtl) n =
    match g with
    ghd :: gtl -> if n = 0 then (g, ghd :: vtl)
        else pair_cons (ghd, vhd) (fill (gtl, vtl) (n - 1))

let drain_tail (g, v) n =
    let rec aux (g, vhd :: vtl) n (gacc, vacc) =
        match g with
        ghd :: gtl -> if n = 0 then (rev gacc @ g, rev vacc @ 0 :: vtl)
            else aux (gtl, vtl) (n - 1) (ghd :: gacc, vhd :: vacc) in
    aux (g, v) n ([], [])

let rec drain (g, vhd :: vtl) n =
    if n = 0 then (g, 0 :: vtl)
    else match g with
        ghd :: gtl -> pair_cons (ghd, vhd) (drain (gtl, vtl) (n - 1))

(* list: init src med dst tl *)
let transfer (g, v) (src, dst) =
    let rec aux (ginit_rev, vinit_rev) (gmed_rev, vmed_rev) (g, v) (src dst) =
        if src = 0 then
            if dst = 0 then match (ginit_rev, vinit_rev, g, v) with
                gihd :: gitl, vihd :: vitl, ghd :: gtl, vhd :: vtl ->
                    let empty_s = gihd - vihd and empty_d = ghd - vhd in
                    (rev ginit_rev @ rev gmed_rev @ g,
                        rev (max 0 (vihd - empty_d) :: vitl) @
                        rev (min ghd (vhd + vihd) :: vmed_rev) @ v)
            else (* TODO *)
