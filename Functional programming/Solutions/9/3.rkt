(define (mk-mobile left right) (cons left right))
(define (mk-branch length struct) (cons length struct))

(define (left-branch mobile) (car mobile))

(define (right-branch mobile) (cdr mobile))

(define (branch-length branch) (car branch))

(define (branch-struct branch) (cdr branch))

(define (total-weight mobile)
    (match mobile
        [(cons (cons len struct) (cons len1 struct1)) (+ (total-weight struct) (total-weight struct1))]
        [weight weight]))

(define (balanced? mobile)
    (match mobile
        [(cons (cons len struct) (cons len1 struct1))
            (and (equal? (* len (total-weight struct)) (* len1 (total-weight struct1))) (balanced? struct) (balanced? struct1))]
        [weight #t]))