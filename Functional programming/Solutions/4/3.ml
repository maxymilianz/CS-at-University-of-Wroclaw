type 'a mtree = MNode of 'a * 'a forest
and 'a forest = EmptyForest | Forest of 'a mtree * 'a forest;;

type 'a mtree_lst = MTree of 'a * ('a mtree_lst) list;;

let breadth (MNode (v, f)) =
    let rec aux = function
        [] -> []
        | EmptyForest :: tl -> aux tl
        | Forest (MNode (v, f0), f1) :: tl -> v :: aux (tl @ [f1; f0]) in
    v :: aux [f]

let breadth_lst (MTree (v, f)) =
    let rec aux = function
        [] -> []
        | MTree (v, f) :: tl -> v :: aux (tl @ f) in
    v :: aux f

let preorder (MNode (v, f)) =
    let rec preord = function
        EmptyForest, labels -> labels
        | Forest (MNode (v, f0), f1), labels ->
            v :: preord (f0, preord (f1, labels)) in
    v :: preord (f, [])

let preorder_lst (MTree (v, f)) =
    let rec preord = function
        [], labels -> labels
        | MTree (v, f) :: tl, labels -> v :: preord (f, preord (tl, labels)) in
    v :: preord (f, [])
