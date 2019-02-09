function fibIter(n) {
    const fibs = [0, 1];

    while (fibs.length < n + 1)
        fibs.push(fibs[fibs.length - 1] + fibs[fibs.length - 2]);

    return fibs[n];
}


function fibRec(n) {
    if (n === 0 || n === 1)
        return n;
    else
        return fibRec(n - 1) + fibRec(n - 2);
}


function test(n) {
    for (let fun of [fibIter, fibRec]) {
        console.time(fun.name);
        fun(n);
        console.timeEnd(fun.name);
    }
}


// console.log(fibIter(44));
// console.log(fibRec(44));

// test(40);

for (let i = 10; i < 20; i++) {
    console.log(i);
    test(i);
}