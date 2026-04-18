


const path = require('node:path');
const RAW_SOURCES = require('../../../config.json').RAW_SOURCES;

module.exports = (code, url) => {
    url = url.split('/');
    url[2] = RAW_SOURCES;
    url = path.join(...url).replaceAll('\\', '/');
    return `
    if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/${url}';
    document.head.appendChild(link);
`;
}