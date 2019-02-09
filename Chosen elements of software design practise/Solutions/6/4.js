const cookieParser = require('cookie-parser');
const http = require('http');
const express = require('express');


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.urlencoded({extended: true}));

app.use(cookieParser('sgs90890s8g90as8rg90as8g9r8a0srg8'));

app.get("/", (req, res) => {
    res.cookie('foo', 'bar');
    res.end("default page");
});

app.get("/faktura/:id", (req, res) => {
    if (req.cookies.foo === 'bar')      // walidacja
        res.end(`dynamicznie generowana faktura: ${req.params.id}`);
    else
        res.end('nie masz uprawnien');
});

app.use((req, res, next) => {
    res.render('404.ejs', {url: req.url});
});

http.createServer(app).listen(3000);