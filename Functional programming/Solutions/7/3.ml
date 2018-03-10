type ('a, 'b) values = {mutable l: ('a * 'b) list}

let empty () = {l = []}

let lookup arg table =
    let rec aux arg l =
        match l with
        [] -> None
        | (arg', val') :: tl -> if arg = arg' then Some val'
            else aux arg tl in
    aux arg table.l

let add value table =
    table.l <- value :: table.l

let rec fib n =
    if n = 0 || n = 1 then n
    else fib (n - 1) + fib (n - 2)

let fib_memo =
    let vals = empty () in
    let rec aux n =
        match lookup n vals with
        None ->
            let v =
                if n = 0 || n = 1 then n
                else aux (n - 1) + aux (n - 2) in
            add (n, v) vals; v
        | Some v -> v in
    aux

let fib_memo' n =
    let vals = Array.make (n + 1) (-1) in
    for i = 0 to n do
        if i = 0 || i = 1 then vals.(i) <- i
        else vals.(i) <- vals.(i - 1) + vals.(i - 2)
    done; vals.(n)

let fib_memo'' n =
    let rec aux n = function
        [] ->
            if n = 0 || n = 1 then [n]
            else (match aux (n - 1) [] with
                [v] -> (match aux (n - 2) [] with
                    [v'] -> [v; v + v'])
                | [v; v'] -> [v'; v + v'])
        | [v] -> [v]
        | [v; v'] -> [v'; v + v'] in
    match aux n [] with
    [v] -> v
    | [v; v'] -> v'

let fib_memo''' n =
    let rec aux n vals =
        if n = 0 || n = 1 then [n]
        else match vals with
            [] -> (match aux (n - 1) [] with
                [v] -> (match aux (n - 2) [] with
                    [v'] -> [v; v + v'])
                | [v; v'] -> [v'; v + v'])
            | [v] -> [v]
            | [v; v'] -> [v'; v + v'] in
    match aux n [] with
    [v] -> v
    | [v; v'] -> v'

(* testing for n = 40 is ok, but difference between memo and memo' is visible ok for
    n = 10000, but then the result is too big for int/long *)
