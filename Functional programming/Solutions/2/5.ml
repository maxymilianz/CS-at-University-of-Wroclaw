let rec concat a l =
    match l with
    [] -> []
    | hd :: tl -> (a :: hd) :: concat a tl

let rec perms l =
    let rec inserts a l =       (* inserts a to l at all possible positions *)
        match l with
        [] -> [[a]]
        | hd :: tl -> (a :: hd :: tl) :: (concat hd (inserts a tl)) in
    let rec insert_to_all a l =     (* inserts a to all of l at all possible positions *)
        match l with
        [] -> []
        | hd :: tl -> inserts a hd @ insert_to_all a tl in
    match l with
    [] -> [[]]
    | hd :: tl -> insert_to_all hd (perms tl)
