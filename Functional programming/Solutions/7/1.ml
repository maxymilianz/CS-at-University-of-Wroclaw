let rec fix f x = f (fix f) x

let factorial_fix = fix (fun f -> fun n -> if n = 0 then 1 else n * (f (n-1)))

let factorial n = let res = ref 1 in
    for i = 2 to n do
        res := !res * i
    done; !res

let fix' f x =
    let aux = ref (fun _ -> failwith "undef") in
    aux := f (fun x -> !aux x); !aux x

let factorial_fix' = fix' (fun f -> fun n -> if n = 0 then 1 else n * (f (n-1)))
