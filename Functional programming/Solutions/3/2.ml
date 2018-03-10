open List

let compute p x =
    let rec aux p x acc =
        match p with
        [] -> acc
        | hd :: tl -> aux tl x (x *. acc +. hd) in
    aux (rev p) x 0.

let compute2 p x =
    let f (x_power, res) a = (x_power *. x, res +. a *. x_power) in
    snd (fold_left f (1., 0.) p)

let compute3 p x =
    fold_right (fun a res -> a +. res *. x) p 0.
