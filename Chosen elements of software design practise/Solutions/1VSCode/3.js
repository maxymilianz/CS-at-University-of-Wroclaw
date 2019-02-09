const ld = require('lodash');


function primes(end) {
    let result = ld.range(2, end);
    let i = 0;

    while (i < result.length) {
        result = result.slice(0, i + 1).concat(result.slice(i + 1).filter(a => a % result[i] !== 0));
        i++;
    }

    return result;
}


console.log(primes(100001));