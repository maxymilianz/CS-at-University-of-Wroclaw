let rec concat a l =
    match l with
    [] -> []
    | hd :: tl -> (a :: hd) :: concat a tl

let rec suffixes l =
    match l with
    [] -> []
    | hd :: tl -> l :: suffixes tl

let rec prefixes l =
    match l with
    [] -> []
    | hd :: tl -> [hd] :: concat hd (prefixes tl)
