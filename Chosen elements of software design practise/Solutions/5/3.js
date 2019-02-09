const http = require('http');


http.createServer((request, response) => {
    response.setHeader('Content-type', 'text/html; charset=utf-8');
    response.setHeader('Content-Disposition', 'attachment');
    response.end(`Hello, world at ${new Date()}!`);
}).listen(3000);