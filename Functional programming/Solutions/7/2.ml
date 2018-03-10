type 'a list_mutable = LMnil | LMcons of 'a * 'a list_mutable ref

let concat_copy l0 l1 =
    let rec aux l0 l1 =
        match l0 with
        LMnil -> ref l1
        | LMcons (hd, tl) -> ref (LMcons (hd, aux !tl l1)) in
    !(aux l0 l1)

let concat_share l0 l1 =
    let rec aux (LMcons (hd, tl)) =
        match !tl with
        LMnil -> tl := l1
        | LMcons (_, _) -> aux !tl in
    aux l0; l0
