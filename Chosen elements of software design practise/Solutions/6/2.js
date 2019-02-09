const express = require('express');
const http = require('http');


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.urlencoded({extended: true}));

app.get('/', (request, response) => {
    response.render('2_index');
});

app.post('/', (request, response) => {
    response.render('2_new_view', {value: 1998});
});

http.createServer(app).listen(3000);