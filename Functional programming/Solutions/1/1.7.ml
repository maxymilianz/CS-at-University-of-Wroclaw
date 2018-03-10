(* 'a -> 'a = <fun> *)
let int_id (x : int) : int = x;
let compose f g x = f (g x);
let rec loop x = loop x;
