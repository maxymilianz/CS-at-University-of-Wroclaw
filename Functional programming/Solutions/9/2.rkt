;;; #lang racket

(define (atom? x)
    (or (number? x)
        (boolean? x)
        (string? x)
        (char? x)
        (symbol? x)))

(define (count-atoms x)
    (match x
        [(cons y z) (+ (count-atoms y) (count-atoms z))]
        [y (if (atom? y) 1 0)]))