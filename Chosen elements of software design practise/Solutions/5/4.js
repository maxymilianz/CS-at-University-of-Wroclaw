const express = require('express');
const http = require('http');


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.urlencoded({extended: true}));

app.get('/', (request, response) => {
    response.render('index', {no_name: false, no_surname: false, no_subject: false});
});

app.post('/', (request, response) => {

    var ex = [];
    for ( var i=0; i<10; i++ ) {
        ex.push(req.body['excercise'+i]);
    }

    const name = request.body.name;

    if (!name)
        response.render('index', {no_name: true});

    const surname = request.body.surname;

    if (!name)
        response.render('index', {no_surname: true});

    const subject = request.body.subject;

    if (!name)
        response.render('index', {no_subject: true});

    const exercise1 = request.body.exercise1;
    const exercise2 = request.body.exercise2;
    const exercise3 = request.body.exercise3;
    const exercise4 = request.body.exercise4;
    const exercise5 = request.body.exercise5;
    const exercise6 = request.body.exercise6;
    const exercise7 = request.body.exercise7;
    const exercise8 = request.body.exercise8;
    const exercise9 = request.body.exercise9;
    const exercise10 = request.body.exercise10;

    response.render('print', {name, surname, subject, exercise1, exercise2, exercise3, exercise4, exercise5, exercise6,
        exercise7, exercise8, exercise9, exercise10});
});

http.createServer(app).listen(3000);