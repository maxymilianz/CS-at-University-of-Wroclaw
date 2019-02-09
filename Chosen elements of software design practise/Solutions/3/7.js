function fib() {
    let [a, b] = [0, 1];

    return {
        next: () => {
            const result = a;
            [a, b] = [b, a + b];
            return {
                value: result,
                done: false
            }
        }
    }
}

const fibIter = {
    [Symbol.iterator]: fib
};

let i = 0;
for (let n of fibIter) {
    console.log(n);
    i++;
    if (i > 6) break;
}

function* fibGen() {
    let [a, b] = [0, 1];

    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

i = 0;
for (let n of fibGen()) {
    console.log(n);
    i++;
    if (i > 6) break;
}