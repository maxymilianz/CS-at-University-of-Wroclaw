const http = require('http');
const express = require('express');


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.urlencoded({extended: true}));

app.get("/", (req, res) => {
    res.end("default page");
});

app.get("/delete/all", (req, res) => {
    res.end('everything deleted by user with permission');
});

app.use((req, res, next) => {
    res.render('404.ejs', {url: req.url});
});

http.createServer(app).listen(3000);