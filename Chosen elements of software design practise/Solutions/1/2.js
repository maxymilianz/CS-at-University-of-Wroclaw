const _ = require('lodash');


function divisibleDigitsAndSum(start, end) {
    function auxSingle(n) {
        const digits = n.toString().split('').map(Number);
        const sum = digits.reduce((a, b) => a + b, 0);
        return n % sum === 0 && digits.every(d => n % d === 0)
    }

    //var a = new Array(100).map((v,i) => i)

    return _.range(start, end).filter(auxSingle);
}


console.log(divisibleDigitsAndSum(1, 100001));