let merge_tail_2 cmp l0 l1 =
    let rec rev l =
        match l with
        [] -> []
        | hd :: tl -> rev tl @ [hd] in
    let rec merge_acc cmp l0 l1 acc =
        match l0, l1 with
        [], [] -> acc
        | [], hd :: tl | hd :: tl, [] -> merge_acc cmp [] tl (hd :: acc)
        | hd0 :: tl0, hd1 :: tl1 ->
            if cmp hd0 hd1 then merge_acc cmp tl0 l1 (hd0 :: acc)
            else merge_acc cmp l0 tl1 (hd1 :: acc) in
    rev (merge_acc cmp l0 l1 [])

let merge_sort_2 cmp l =
    let rec merge_sort_aux cmp l =
        match l with
        [] -> []
        | hd :: tl -> merge_tail_2 cmp [hd] (merge_sort_aux cmp tl) in
    merge_sort_aux cmp l

let rec merge cmp l0 l1 =
    match l0 with
    [] -> l1
    | hd0 :: tl0 ->
        match l1 with
        [] -> l0
        | hd1 :: tl1 ->
            if cmp hd0 hd1 then hd0 :: merge cmp tl0 l1
            else hd1 :: merge cmp l0 tl1

let merge_tail cmp l0 l1 =
    let rec merge_acc cmp l0 l1 acc =
        match l0 with
        [] -> acc @ l1
        | hd0 :: tl0 ->
            match l1 with
            [] -> acc @ l0
            | hd1 :: tl1 ->
                if cmp hd0 hd1 then merge_acc cmp tl0 l1 (acc @ [hd0])
                else merge_acc cmp l0 tl1 (acc @ [hd1]) in
    merge_acc cmp l0 l1 []

let rec merge_sort cmp l =
    match l with
    [] -> []
    | hd :: tl -> merge_tail cmp [hd] (merge_sort cmp tl)

(* Najpierw zrobilem merga, ktory nie odwraca, a potem ponizszego. *)

let merge_rev cmp l0 l1 =
    let rec merge_acc cmp l0 l1 acc =
        match (l0, l1) with
        ([], []) -> acc
        | (hd :: tl, []) -> merge_acc cmp tl l1 (hd :: acc)
        | ([], l) -> merge_acc cmp l1 l0 acc
        | (hd0 :: tl0, hd1 :: tl1) ->
            if cmp hd0 hd1 then merge_acc cmp tl0 l1 (hd0 :: acc)
            else merge_acc cmp l0 tl1 (hd1 :: acc) in
    let rec rev l =
        match l with
        [] -> []
        | hd :: tl -> rev tl @ [hd] in
    rev (merge_acc cmp l0 l1 [])

let rec merge_sort_rev cmp l =
    match l with
    [] -> []
    | hd :: tl -> merge_rev cmp [hd] (merge_sort_rev cmp tl)
