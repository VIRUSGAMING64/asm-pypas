const imports = require('./imports');
const jsx = require('./jsx');

module.exports = (code, currentUrl, swap = {}) => {
    return imports(jsx(code), currentUrl, swap);
};