(define (deriv expr var)
    (match expr
        [`(* ,l ,r) (let ([dl (deriv l var)] [dr (deriv r var)])
            (let ([new_l (if (or (zero? l) (zero? dl)) 0)]
                [new_r (if (or (zero? r) (zero? dr)) 0)])
                (if (zero? new_l) new_r (if (zero? new_r) new_l `(+ new_l new_r))))]
        [`(+ ,l ,r) `(+ ,(deriv l var) ,(deriv r var))]
        [x (if (equal? x var) 1 0)]))

`(+ (* ,(deriv l var) ,r) (* ,l ,(deriv r var)))