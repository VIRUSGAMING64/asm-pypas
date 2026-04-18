const { PORT } = require('../../config.json');
const SRC = require('./urls/src');
const PUBLIC = require('./urls/public');
const APP = require('./urls/app');
const LIBS = require('./urls/libs');


module.exports = () => {
    const express = require('express');
    const app = express();
    app.use((req, res, next) => {
        //console.log(req.method, req.url);
        next();
    })

    SRC(app); // sources and code compiling
    PUBLIC(app); // public and static files
    APP(app); // app page
    LIBS(app) // libs

    app.listen(PORT);
    console.log('\x1b[33m\x1b[1mRunning development server on:', '\x1b[30mhttp://localhost:' + PORT + '/', ' \x1b[0m');
}