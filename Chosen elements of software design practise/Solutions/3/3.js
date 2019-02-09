function forEach(a, f) {
    for (e of a)
        f(e);
}

function map(a, f) {
    const result = [];

    for (e of a)
        result.push(f(e));

    return result;
}

function filter(a, f) {
    const result = [];
    for (e of a) if (f(e)) result.push(e);
    return result;
}

const a = [1, 2, 3, 4];
forEach(a, e => { console.log(e); });
console.log(filter(a, e => e < 3));
console.log(map(a, e => e * 2));