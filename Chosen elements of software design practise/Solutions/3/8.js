function* take(it, top) {
    let i = 0;

    for (let n of it) {
        yield n;
        i++;
        if (i >= top) break;
    }
}

function* fibGen() {
    let [a, b] = [0, 1];

    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

for (let n of take(fibGen(), 8)) console.log(n);