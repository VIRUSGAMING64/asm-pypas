const fs = require('node:fs');
const path = require('node:path');
const compiler = require('../../compiler');

const { SOURCES_PATH, SOURCES_URL, SERVER_URL, RAW_SOURCES } = require('../../../config.json');
const types = require('../../mimetypes.json');

module.exports = (app) => {
    var regex = `${path.join(SERVER_URL, SOURCES_URL).replaceAll('\\', '\\/')}.`;

    regex = new RegExp(regex);

    app.get(regex, (req, res, next) => {
        var pth = req.url.split('/');
        pth[0] = '';
        pth[1] = '';
        pth[2] = '';

        pth = path.join(SOURCES_PATH, ...pth).replaceAll('\\', '/');
        var ext = path.extname(pth);

        try {
            var content = fs.readFileSync(pth);
            ext = ext.replace('.', '');

            var { code, type } = compiler.transform(content, ext, req.url);


            res.writeHead(200, { 'content-type': types['.' + type] });
            res.end(code);

        } catch (error) {
            next();
        }
    });

    var regex2 = `${path.join(SERVER_URL, RAW_SOURCES).replaceAll('\\', '\\/')}.`;

    regex2 = new RegExp(regex2);
    app.get(regex2, (req, res, next) => {
        var pth = req.url.split('/');
        pth[0] = '';
        pth[1] = '';
        pth[2] = '';

        pth = path.join(SOURCES_PATH, ...pth).replaceAll('\\', '/');
        var ext = path.extname(pth);

        try {
            var content = fs.readFileSync(pth);
            ext = ext.replace('.', '');

            var { code, type } = { code: content, type: ext };


            res.writeHead(200, { 'content-type': types['.' + type] });
            res.end(code);

        } catch (error) {
            next();
        }
    });
};