const cookieParser = require('cookie-parser');
const express = require('express');
const http = require('http');
const session = require('express-session');
const fileStore = require('session-file-store')(session);


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.disable('etag');

app.use(session({
    store: new fileStore(),
    secret: 'keyboard cat'
}));

app.get('/', (request, response) => {
    response.render('3_index_session');
});

app.post('/', (request, response) => {
    if (!request.session.sessionValue)      // to można też usuwać
        request.session.sessionValue = new Date().toString();
    console.log(request.session.sessionValue);
    response.render('3_index_session', {sessionValue: request.session.sessionValue});
});

http.createServer(app).listen(3000);