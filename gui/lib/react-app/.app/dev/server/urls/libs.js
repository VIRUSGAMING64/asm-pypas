const fs = require('node:fs');
const path = require('node:path');
const { SERVER_URL, SOURCES_URL, SERVER_PATH } = require('../../../config.json');
const urlify = (p) => path.join(p).replace(/\\/g, '/');;

module.exports = (app) => {
    app.get(urlify(path.join(SERVER_URL, SOURCES_URL, 'react.js')), (req, res) => {
        res.writeHead(200, { 'content-type': 'application/javascript' });
        res.end(fs.readFileSync(path.join(SERVER_PATH, '/react/react.js'), 'utf-8'));
    });
    app.get(urlify(path.join(SERVER_URL, SOURCES_URL, 'react-dom.js')), (req, res) => {
        res.writeHead(200, { 'content-type': 'application/javascript' });
        res.end(fs.readFileSync(path.join(SERVER_PATH, '/react/react-dom.js'), 'utf-8'));
    });
}