module type PQUEUE = sig
    type priority
    type 'a t

    exception EmptyPQueue

    val empty : 'a t
    val insert : 'a t -> priority -> 'a -> 'a t
    val remove : 'a t -> priority * 'a * 'a t
end

module PQueue : PQUEUE with type priority = int = struct
    type priority = int
    type 'a t = ('a * priority) list

    exception EmptyPQueue

    let empty = []

    let rec insert q p e =
        match q with
        [] -> [e, p]
        | hd :: tl ->
            match hd with
            e', p' ->
                if p < p' then hd :: insert tl p e
                else (e, p) :: q

    let remove = function
        [] -> raise EmptyPQueue
        | (e, p) :: tl -> p, e, tl
end

let sort l =
    let rec create_queue q = function
        [] -> q
        | hd :: tl -> create_queue (PQueue.insert q hd hd) tl in
    let rec queue_to_list q =
        try
            match PQueue.remove q with
            _, e, q' -> e :: queue_to_list q'
        with
            PQueue.EmptyPQueue -> [] in
    List.rev (queue_to_list (create_queue PQueue.empty l))

module type ORDTYPE = sig
    type t
    type comparison = LT | EQ | GT
    val compare : t -> t -> comparison
end

module OrdPQueue (OrdType : ORDTYPE) : PQUEUE with type priority = OrdType.t = struct
    type priority = OrdType.t
    type 'a t = ('a * priority) list

    exception EmptyPQueue

    let empty = []

    let rec insert q p e =
        match q with
        [] -> [e, p]
        | hd :: tl ->
            match hd with
            e', p' ->
                if OrdType.(compare p p' = LT) then hd :: insert tl p e
                else (e, p) :: q

    let remove = function
        [] -> raise EmptyPQueue
        | (e, p) :: tl -> p, e, tl
end

module OrdInt : ORDTYPE with type t = int = struct
    type t = int
    type comparison = LT | EQ | GT
    let compare a b =
        if a < b then LT
        else if a = b then EQ
        else GT
end

module IntPQueue = OrdPQueue(OrdInt)

let sort' l =
    let rec create_queue q = function
        [] -> q
        | hd :: tl -> create_queue (IntPQueue.insert q hd hd) tl in
    let rec queue_to_list q =
        try
            match IntPQueue.remove q with
            _, e, q' -> e :: queue_to_list q'
        with
        IntPQueue.EmptyPQueue -> [] in
    List.rev (queue_to_list (create_queue IntPQueue.empty l))

let sort'' (type t') (module OrdType : ORDTYPE with type t = t') l =
    let module PQueue = OrdPQueue(OrdType) in
    let rec create_queue q = function
        [] -> q
        | hd :: tl -> create_queue (PQueue.insert q hd hd) tl in
    let rec queue_to_list q =
        try
            match PQueue.remove q with
            _, e, q' -> e :: queue_to_list q'
        with
        PQueue.EmptyPQueue -> [] in
    List.rev (queue_to_list (create_queue PQueue.empty l))

(* sort'' (module OrdInt) <list> *)
