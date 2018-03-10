open List

type 'a place = Place of ('a list * 'a list)
(* kth place representation of n-element list is:
    Place (k-1, k-2, ..., 0), (k, k+1, ..., n-1) *)

let find_nth l n =
    let rec aux l n acc =
        if n <= 0 then (acc, l)
        else match l with
            hd :: tl -> aux tl (n - 1) (hd :: acc) in
    let place = aux l n [] in
    Place place

let collapse (Place (rev_init, tl)) = rev rev_init @ tl

let add a (Place (rev_init, tl)) = Place (rev_init, a :: tl)

let del (Place (rev_init, hd :: tl)) = Place (rev_init, tl)

let next (Place (rev_init, hd :: tl)) = Place (hd :: rev_init, tl)

let prev (Place (hd :: tl_r_i, tl)) = Place (tl_r_i, hd :: tl)

type 'a btree = Leaf | Node of 'a btree * 'a * 'a btree

type 'a btplace = Place of (('a btree * bool) list * 'a btree)
(*  (btree * bool) list - reversed list of nodes skipped and info if skipped
    node was left or right second tree - tree from current node *)
