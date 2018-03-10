let lit s c = fun s' -> c (s' ^ s)

let eol c = fun s -> c (s ^ "\n")

let inr c s = fun n -> c (s ^ string_of_int n)

let flt c s = fun fl -> c (s ^ string_of_float fl)

let str c s = fun s' -> c (s ^ s')

let (++) f0 f1 c0 = f0 (f1 c0)

let sprintf f = f (fun v -> v) ""

let example n =
    sprintf (lit "Ala ma " ++ inr ++ lit " kot" ++ str ++ lit "." ++ eol) n
        (if n = 1 then "a" else if 1 < n && n < 5 then "y" else "ow")
