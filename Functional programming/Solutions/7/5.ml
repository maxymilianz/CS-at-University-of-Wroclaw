type 'a lnode = {value: 'a; mutable next: 'a lnode}

let make_single v =
    let rec l = {value = v; next = l} in
    l

let ins_hd hd l =
    let l' = {value = hd; next = l.next} in
    l.next <- l'; l

let ins_last last l =
    let l' = {value = last; next = l.next} in
    l.next <- l'; l'

let rm_hd l = l.next <- (l.next).next; l

let make n =
    let l = ref (make_single 1) in
    for i = 2 to n do
        l := ins_last i !l
    done; !l

let rec nth n l =
    if n = 1 then l
    else nth (n - 1) l.next

let josephus n m =
    let l = make n in
    let rec aux l rev_perm =
        if l == l.next then l.value :: rev_perm
        else let l = nth m l in
            let hd = (l.next).value in
            aux (rm_hd l) (hd :: rev_perm) in
    List.rev (aux l [])
