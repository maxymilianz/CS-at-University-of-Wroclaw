const fs = require('fs');
const util = require('util');

const path = '5.js';
const encoding = 'utf-8';

// fs.readFile(path, encoding, (error, data) => { console.log(data) });

function fsPromise(path, options) {
    return new Promise((resolve, reject) => {
        fs.readFile(path, options, (error, data) => {
            if (error)
                reject(error);
            resolve(data);
        })
    })
}

// fsPromise(path, encoding).then(console.log).catch(console.log);

// util.promisify(fs.readFile)(path, encoding).then(console.log).catch(console.log);

// fs.promises.readFile(path, encoding).then(console.log).catch(console.log);

(async function test() {
    const data = await util.promisify(fs.readFile)(path, encoding);
    console.log(data);
})();

// w realnej aplikacji warto używać try-catch