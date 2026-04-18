const babel = require('@babel/core');

module.exports = (code) => babel.transform(code, { presets: ['@babel/preset-react'] }).code;