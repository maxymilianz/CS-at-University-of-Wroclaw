function createGenerator(n) {
    let state = 0;
    return {
        next: function () {
            return {
                value: state,
                done: state++ >= n
            }
        }
    }
}

const foo = {
    [Symbol.iterator]: () => createGenerator(4)
};

const foo1 = {
    [Symbol.iterator]: () => createGenerator(8)
};

for (let f of foo) console.log(f);
for (let f of foo1) console.log(f);