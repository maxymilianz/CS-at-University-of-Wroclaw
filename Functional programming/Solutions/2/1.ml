let rec concat_and_not a l =
    match l with
    [] -> []
    | hd :: tl -> (a :: hd) :: hd :: concat_and_not a tl

let rec sublists l =
    match l with
    [] -> []
    | hd :: tl -> [hd] :: concat_and_not hd (sublists tl)
