const fs = require('node:fs');
const path = require('node:path');

const { PUBLIC_PATH, PUBLIC_URL, SERVER_URL } = require('../../../config.json');
const types = require('../../mimetypes.json');


module.exports = (app) => {
    var regex = `${path.join(SERVER_URL, PUBLIC_URL).replaceAll('\\', '\\/')}.`;
    regex = new RegExp(regex);

    app.get(regex, (req, res) => {

        var pth = req.url.split('/');
        pth[0] = '';
        pth[1] = '';
        pth[2] = '';

        pth = path.join(PUBLIC_PATH, ...pth).replaceAll('\\', '/');

        try {
            var content = fs.readFileSync(pth);
            var type = types[path.extname(pth)] || 'text/plain';
            res.writeHead(200, { 'content-type': type });
            res.end(content);

        } catch (error) {
            res.writeHead(404, { 'content-type': 'text/plain' });
            res.end('' + error);
        }
    });
}