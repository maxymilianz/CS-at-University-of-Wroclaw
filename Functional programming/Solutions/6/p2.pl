p(a) :- p(b), (p(c); p(d)), p(e).
p(b) :- p(d).
p(d).
p(e) :- p(d).