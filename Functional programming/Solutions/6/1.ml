type 'a btree = Leaf of 'a | Node of 'a btree * 'a btree

let rec to_list = function
    Leaf v -> [v]
    | Node (l, r) -> to_list l @ to_list r

let join t0 t1 = Node (t0, t1)

let join_aux t_opt t =
    match t_opt with
    None -> Some t
    | Some t' -> Some (join t' t)

let samefringe t0 t1 = to_list t0 = to_list t1

let samefringe' t0 t1 =
    let rec aux t0 t1 =
        match t0, t1 with
        Leaf v0, Leaf v1 -> (v0 = v1, None, None)
        | Leaf v, Node (l, r) -> (match aux (Leaf v) l with
            (success, None, t) -> (success, None, join_aux t r))
        | Node (l, r), Leaf v -> (match aux l (Leaf v) with
            (success, t, None) -> (success, join_aux t r, None))
        | Node (l0, r0), Node (l1, r1) -> match aux l0 l1 with
            (success, t0, t1) ->
                if success then
                    match (join_aux t0 r0), (join_aux t1 r1) with
                    Some t0, Some t1 -> aux t0 t1
                else (false, None, None) in
    match aux t0 t1 with
    (success, None, None) -> success
    | _ -> false
