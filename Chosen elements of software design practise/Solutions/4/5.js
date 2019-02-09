const lineReader = require('readline').createInterface(process.stdin, process.stdout);


lineReader.question('Enter your name:\n', name => {
    console.log('Hello, ' + name + '!');
    process.exit();
});