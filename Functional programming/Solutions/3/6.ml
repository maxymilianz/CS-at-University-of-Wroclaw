(* nie potrafie powiedziec jakie to liczby - istnieje wiecej niz 1 para
    a, b : 1 < a < b, a+b < 100, ab = xy
wiedzialem o tym - dla wszystkich par c, d : 1 < c < d, c+d = x+y,
    (istnieje inna para e, f : cd = ef, 1 < e < f)
a to w takim razie juz potrafie - istnieje dokladnie 1 para
    a, b : 1 < a < b, a+b < 100, ab = xy, (dla wszystkich par
    c, d : 1 < c < d, c+d = a+b, (istnieje inna para
    e, f : cd = ef, 1 < e < f))
ja juz tez - istnieje dokladnie 1 para
    c, d : 1 < c < d, c+d = x+y, (istnieje dokladnie 1 para a, b : 1 < a < b,
    a+b < 100, ab = cd, (dla wszystkich par c, d : 1 < a < b, c+d = a+b,
    (istnieje inna para e, f : cd = ef, 1 < e < f))) *)

open List

let range n =
    let rec range i =
        if i = n then []
        else i :: range (i + 1) in
    range 0

let rec drop n l =
    if n = 0 then l
    else match l with
    hd :: tl -> drop (n - 1) tl

let int_root square = int_of_float (sqrt (float square))

let divs_gt1_neq n =
    let root = int_root n in
    let rec divs d =
        if d >= root then []
        else if n mod d = 0 then (d, n / d) :: divs (d + 1)
        else divs (d + 1) in
    divs 2

let sums_gt1_neq n =
    let half = n / 2 in
    let rec sums a =
        if a >= half then []
        else (a, n - a) :: sums (a + 1) in
    sums 2

let pair_to_sum (x, y) = x + y

let pair_to_prod (x, y) = x * y

let more_1_prod prod =
    length (divs_gt1_neq prod) > 1

let duplicate_sums sum =
    for_all more_1_prod (map pair_to_prod (sums_gt1_neq sum))

let prod_match prod =
    length (filter duplicate_sums (map pair_to_sum (divs_gt1_neq prod))) = 1

let sum_match sum =
    length (filter prod_match (map pair_to_prod (sums_gt1_neq sum))) = 1

let both_match (x, y) = sum_match (x + y) && prod_match (x * y)

let solution =
    filter both_match (flatten (map sums_gt1_neq (drop 5 (range 100))))
