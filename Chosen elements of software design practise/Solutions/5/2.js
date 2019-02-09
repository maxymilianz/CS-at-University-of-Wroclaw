const fs = require('fs');
const https = require('https');


(async function() {
    const pfx = await fs.promises.readFile('2.pfx');
    https.createServer({pfx: pfx, passphrase: '568923bbb'}, (req, res) => {
        res.setHeader('Content-type', 'text/html; charset=utf-8');
        res.end(`Hello, world at ${new Date()}!`);
    }).listen(3000);
})();