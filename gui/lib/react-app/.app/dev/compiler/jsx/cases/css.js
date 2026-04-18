const path = require('node:path');

module.exports = ($, url, currentUrl) => {
    url = url.split('/');
    url = url.join('/').startsWith('./') ? path.join(currentUrl, ...url).replaceAll('\\', '/') : path.join(...url).replaceAll('\\', '/');
    return `(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '${url}';
        document.head.appendChild(link);})();
    `;
}