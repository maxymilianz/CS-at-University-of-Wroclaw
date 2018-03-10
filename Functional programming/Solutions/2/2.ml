let rec a n =
    if n = 0 then 0
    else 2 * a (n - 1) + 1

let a_tail n =
    let rec a i n acc =
        if i = n then acc
        else a (i + 1) n (2 * acc + 1) in
    a 0 n 0

(* dla n = 1 000 000 wynik a to stack overflow, a a_tail -1, bo zakres longa *)
