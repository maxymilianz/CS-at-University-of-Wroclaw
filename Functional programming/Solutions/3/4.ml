open List

let square m =
    let len = length m in
    for_all ((=) len) (map length m)

let rec column m n =
    fold_right (fun m res -> nth m n :: res) m []

let transposition m =
    mapi (fun i row -> column m i) m

let rec zip l0 l1 =
    match l0, l1 with
    [], [] -> []
    | hd0 :: tl0, hd1 :: tl1 -> (hd0, hd1) :: zip tl0 tl1

let zip1 = combine

let zipf l0 l1 f =
    let rec f_pair l f =
        match l with
        [] -> []
        | (l, r) :: tl -> f l r :: f_pair tl f in
    f_pair (zip l0 l1) f

let zipf1 l0 l1 f =
    map (fun (a, b) -> f a b) (zip1 l0 l1)

let mult_vec v m =
    let rec mult v m =
        match m with
        [] -> []
        | hd :: tl -> fold_left (+) 0 (zipf v hd ( *)) :: mult v tl in
    mult v (transposition m)

let mult_vec1 v m =
    let mult v0 v1 = fold_left (+) 0 (zipf v0 v1 ( *)) in
    map (mult v) (transposition m)

let rec mult_mtx m0 m1 =
    match m0 with
    [] -> []
    | hd :: tl -> mult_vec hd m1 :: mult_mtx tl m1

let mult_mtx1 m0 m1 = map ((fun m v -> mult_vec1 v m) m1) m0
