const cookieParser = require('cookie-parser');
const express = require('express');
const http = require('http');


let cookie_exists = false;

const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.urlencoded({extended: true}));

app.use(cookieParser('sgs90890s8g90as8rg90as8g9r8a0srg8'));

app.get('/', (request, response) => {
    response.render('3_index');
});

app.post('/', (request, response) => {
    if (cookie_exists) {
        console.log(request.cookies.foo);
        response.cookie('foo', 'bar', {expires: new Date()})
    }
    else {
        response.cookie('foo', 'bar');
    }

    cookie_exists = !cookie_exists;
    response.render('3_index');
});

http.createServer(app).listen(3000);