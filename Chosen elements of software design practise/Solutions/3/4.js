function createFs(n) {
    const fs = [];

    for (var i = 0; i < n; i++) {
        fs[i] = (k => () => k)(i);
    }

    return fs;
}

const myFs = createFs(2);
console.log(myFs[0]());
console.log(myFs[1]());

// zmienna zadeklarowana przy pomocy 'let' jest widoczna lokalnie dla bloku (for), a z 'var' - dla funkcji