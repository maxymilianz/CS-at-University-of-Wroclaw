let numbers =
    let n = ref 0 in
    function None -> n := !n + 1; !n
        | Some v -> n := v; !n

let fresh s = s ^ string_of_int (numbers None)

let reset n = numbers (Some n); ()
