let compose f g x = f (g x);;
let rec iterate n f x =
    if n <= 0 then x
    else compose (iterate (n - 1) f) f x;;
let mul x y = iterate y ((+) x) 0;;
let pow x y = iterate y (( *) x) 1;;
let (^) = pow
