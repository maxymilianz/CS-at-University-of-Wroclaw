open List

let derivative p =
    let rec aux p n =
        match p with
        [] -> []
        | hd :: tl -> hd *. n :: aux tl (n +. 1.) in
    match p with
    [] | [_] -> []
    | hd :: tl -> aux tl 1.

let derivative2 p =
    match p with
    [] | [_] -> []
    | hd :: tl -> mapi (fun n a -> (float (n + 1)) *. a) tl
