module type VERTEX = sig
    type t
    type label

    val equal : t -> t -> bool
    val create : label -> t
    val label : t -> label
end

module type EDGE = sig
    type t
    type vertex
    type label

    val vertexes : t -> vertex * vertex
    val equal : t -> t -> bool
    val create : label -> vertex -> vertex -> t
    val label : t -> label
end

module Vertex : VERTEX with type t = int = struct
    type t = int
    type label = int

    let equal v0 v1 = v0 = v1

    let create l = l

    let label v = v
end

module Edge : EDGE with type label = int and type vertex = Vertex.t = struct
    type vertex = Vertex.t
    type t = int * vertex * vertex
    type label = int

    let vertexes (_, v0, v1) = (v0, v1)

    let equal e0 e1 = e0 = e1

    let create l v0 v1 = (l, v0, v1)

    let label (e, _, _) = e
end

module type GRAPH = sig
    (* typ reprezentacji grafu *)
    type t

    module V : VERTEX
    type vertex = V.t

    module E : EDGE with type vertex = vertex

    type edge = E.t

    (* funkcje wyszukiwania *)
    val mem_v : t -> vertex -> bool
    val mem_e : t -> edge -> bool
    val mem_e_v : t -> vertex -> vertex -> bool
    val find_e : t -> vertex -> vertex -> edge
    val succ : t -> vertex -> vertex list
    val pred : t -> vertex -> vertex list
    val succ_e : t -> vertex -> edge list
    val pred_e : t -> vertex -> edge list

    (* funkcje modyfikacji *)
    val empty : t
    val add_e : t -> edge -> t
    val add_v : t -> vertex -> t
    val rem_e : t -> edge -> t
    val rem_v : t -> vertex -> t

    (* iteratory *)
    val fold_v : (vertex -> 'a -> 'a) -> t -> 'a -> 'a
    val fold_e : (edge -> 'a -> 'a) -> t -> 'a -> 'a
end

module Graph : GRAPH with module V = Vertex and module E = Edge = struct
    module V = Vertex
    type vertex = V.t

    module E = Edge
    type edge = E.t

    type t = (vertex * vertex list) list

    let rec mem_v g v =
        match g with
        [] -> false
        | (v', _) :: tl -> v = v' || mem_v tl v

    let mem_e g e =
        let v0, v1 = Edge.vertexes e in
        let rec mem_vertex v = function
            [] -> false
            | v' :: tl -> v = v' || mem_vertex v tl in
        let rec aux = function
            [] -> false
            | (v, l) :: tl ->
                if v = v0 then mem_vertex v1 l
                else aux tl in
        aux g

    let mem_e_v g v0 v1 =
        let e = Edge.create 0 v0 v1 in
        mem_e g e

    let find_e g v0 v1 =
        Edge.create 0 v0 v1

    let rec succ ((v', l) :: tl) v =
        if v' = v then l
        else succ tl v

    let pred g v =
        let rec mem_vertex v = function
            [] -> false
            | v' :: tl -> v = v' || mem_vertex v tl in
        let rec aux = function
            [] -> []
            | (v', l) :: tl ->
                if mem_vertex v l then v' :: aux tl
                else aux tl in
        aux g

    let succ_e g v = List.map (Edge.create 0 v) (succ g v)

    let pred_e g v = List.map (fun v' -> Edge.create 0 v' v) (pred g v)

    let empty = []

    let add_e g e =
        let v0, v1 = Edge.vertexes e in
        let rec add_v l =
            match l with
            [] -> [v1]
            | v :: tl ->
                if v = v1 then l
                else v :: add_v tl in
        let rec find_v = function
            [] -> [v0, [v1]]
            | hd :: tl ->
                match hd with
                v, l ->
                    if v = v0 then (v, add_v l) :: tl
                    else hd :: find_v tl in
        find_v g

    (* let rec add_v g v =
        match g with
        [] -> [g, []]
        | hd :: tl ->
            match hd with
            v', _ ->
                if v = v' then g
                else hd :: add_v tl v *)

    let add_v g v = g

    let rem_e g e =
        let v0, v1 = Edge.vertexes e in
        let rec rem_v = function
            [] -> []
            | v :: tl ->
                if v = v1 then tl
                else v :: rem_v tl in
        let rec find_v = function
            [] -> []
            | hd :: tl ->
                match hd with
                v, l ->
                    if v = v0 then (v, rem_v) :: tl
                    else hd :: find_v tl in
        find_v g

    let rec rem_v g v =
        let rec rem = function
            [] -> []
            | v' :: tl ->
                if v = v' then tl
                else v' :: rem tl in
        match g with
        [] -> []
        | (v', l) :: tl->
            if v = v' then tl
            else (v', rem l) :: rem_v tl v

    let rec fold_v f g i =
        match g with
        [] -> i
        | (v, _) :: tl -> f v (fold_v f tl i)

    let fold_e f g i = i
end
