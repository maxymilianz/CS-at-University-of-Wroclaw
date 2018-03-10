type 'a btree = Leaf | Node of 'a btree * 'a * 'a btree

type 'a array = Array of 'a btree * int

let aempty = Array (Leaf, 0)

let asub (Array (t, _)) n =
    let rec aux (Node (l, v, r)) n =
        if n = 1 then v
        else if n mod 2 = 0 then aux l (n / 2)
        else aux r (n / 2) in
    aux t n

let aupdate (Array (t, count)) n v' =
    let rec aux (Node (l, v, r)) n v' =
        if n = 1 then Node (l, v', r)
        else if n mod 2 = 0 then Node (aux l (n / 2) v', v, r)
        else Node (l, v, aux r (n / 2) v') in
    Array (aux t n v', count)

let ahiext (Array (t, count)) v =
    let rec aux t n v =
        if n = 1 then Node (Leaf, v, Leaf)
        else match t with
            Node (l, v', r) -> if n mod 2 = 0 then Node (aux l (n / 2) v, v', r)
                else Node (l, v', aux r (n / 2) v) in
    let count' = count + 1 in
    Array (aux t count' v, count')

let ahirem (Array (t, count)) =
    let rec aux (Node (l, v, r)) n =
        if n = 1 then Leaf
        else if n mod 2 = 0 then Node (aux l (n / 2), v, r)
        else Node (l, v, aux r (n / 2)) in
    Array (aux t count, count - 1)
