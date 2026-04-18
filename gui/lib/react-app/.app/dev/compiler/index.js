const jsx = require('./jsx'); //! ERROR CUANDO HAY IMPORT DENTRO DE UN STRING O COMENTARIO, ARREGLAR

const types = {
    jsx: [jsx, 'js']
};

module.exports = {
    transform: (code, type, url, swap={}) => {
        return types[type] ? { code: types[type][0](code, url, swap), type: types[type][1] } : { code, type };
    }
}