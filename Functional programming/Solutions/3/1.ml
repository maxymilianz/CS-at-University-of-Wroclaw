open List

let compute p x =
    let rec aux p acc =
        match p with
        [] -> acc
        | hd :: tl -> aux tl (x *. acc +. hd) in
    aux p 0.

let compute2 p x =
    let f a (x_power, res) = (x_power *. x, res +. a *. x_power) in
    snd (fold_right f p (1., 0.))

let compute3 p x =
    fold_left (fun res a -> res *. x +. a) 0. p
