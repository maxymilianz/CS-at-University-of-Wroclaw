// taka memoizacja (jak na wykładzie) nie ma wiele sensu, bo zapamiętuje tylko pierwsze wywołanie funkcji
function memoize(fun) {
    const cache = {};
    
    return function (n) {
        if (n in cache)
            return cache[n];

        const result = fun(n);
        cache[n] = result;
        return result;
    }
}

function fib(n) {
    if (n < 2)
        return n;

    return fib(n - 1) + fib(n - 2);
}

fib = memoize(fib);
console.log(fib(410));
//
// function sensibleFibMemo() {
//     const cache = {};
//
//     const fibMemo = function (n) {
//         if (n < 2)
//             return n;
//         if (n in cache)
//             return cache[n];
//
//         const result = fibMemo(n - 1) + fibMemo(n - 2);
//         cache[n] = result;
//         return result;
//     };
//
//     return fibMemo;
// }
//
// fibMemo = sensibleFibMemo();
// console.log(fibMemo(41));