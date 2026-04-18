const path = require('node:path');
module.exports = ($, url, currentUrl) => {
    $ = $.split(' ');
    const var_name = $[1];
    return `const ${var_name} = "${path.join(currentUrl, url).replaceAll('\\', '/')}";`
}