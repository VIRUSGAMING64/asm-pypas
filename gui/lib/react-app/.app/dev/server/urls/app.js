const fs = require('node:fs');
const path = require('node:path');
const jsx = require('./jsx');
const transform = require('../../compiler/jsx')

const { APP_PATH, SERVER_PATH, PAGE_NAME, LAYOUT_NAME } = require('../../../config.json');
var dir = path.dirname(PAGE_NAME)



function getRutes(dir) {
    var rutes = [];
    fs.readdirSync(dir).map((e) => {
        var p = path.join(dir, e);

        if (fs.statSync(p).isFile()) {
            rutes.push(path.join(path.parse(p).dir, path.parse(p).name).replaceAll('\\', '/'));
        } else {
            rutes.push(...getRutes(p));
        }


    });
    return rutes
}

var names = getRutes(dir+"/app");
console.log(dir)
names = names.map(url => url.replace('app/', '')); //! temporal

module.exports = (app) => {

    names.map(name => {
        
        var url = name.split("/")
        url.splice(0, 2)
        url = url.join("/")
        console.log(url)

        var endp = name.split('/')[name.split('/').length - 1];
        console.log(endp)
        app.get(`/${url}`, (req, res) => {
            var page = jsx.render(path.join(APP_PATH, LAYOUT_NAME), { imports: { 'app/': path.join(SERVER_PATH, 'components/') }, default: 'jsx' }, { name:url});
            res.writeHead(200, { 'content-type': 'text/html' });
            res.end(page);
        })
        app.get(`/_server/sites/${url}.js`, (req, res) => {
            res.writeHead(200, { 'content-type': 'application/javascript' });
            res.end(transform(fs.readFileSync(path.join("../../app/", url + '.jsx'), 'utf-8'), `/_server/src/${endp}.js`));
        });
    })
}