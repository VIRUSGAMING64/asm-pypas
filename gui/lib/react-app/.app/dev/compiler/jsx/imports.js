const path = require('node:path');
const { SERVER_URL, SOURCES_URL, PUBLIC_URL } = require('../../../config.json');
const urlify = require('./src/urlify');
const urlFrom = require('./src/urlfrom');
const imports = require('./src/imports');
const cases = require('./cases');


module.exports = (code, currentUrl, swap) => {

    currentUrl = path.dirname(currentUrl);
    const r = ($) => {
        $ = $.split(' ');

        let url = $[$.length - 1].replace(/\"|\'/gi, ''); // delete " or ' from the url;
        $.splice($.length - 1, 1);
        $ = $.join(' ');

        if (url.startsWith('/') ? 0 : 1) { // find in sources
            url = urlFrom(url, imports);
            url = path.parse(url);
            url = (path.join(url.dir, url.name) + (swap[url.ext] ? swap[url.ext] : url.ext));

            url = urlify(url);
            !url.startsWith('/') ? url = './' + url : 0;

            const type = path.extname(url).replace('.', '');

            return cases($, url, type, currentUrl);
        } else { // find in public
            url = path.join(SERVER_URL, PUBLIC_URL, url);
            url = urlify(url);
            const type = path.extname(url).replace('.', '');

            return cases($, url, type, '');
        }
    }

    return code.replace(/import .+ from \'.+\'|import .+ from \".+\"|import .+ from \`.+\`/gi, r).replace(/import \'.+\'|import \".+\"|import \`.+\`/gi, r)
};