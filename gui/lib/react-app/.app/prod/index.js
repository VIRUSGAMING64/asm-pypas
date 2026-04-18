const dir = process.argv[2];
console.log('\x1b[32m\x1b[1m\nStarting server...', ' \x1b[0m');
const t = Date.now();

const express = require('express');
const { IPv4 } = require('ipaddr.js');
const server = express();
const static = express.static(dir);
const path = require('path');
const fs = require('node:fs');
const PORT = require('../config.json').PORT;


console.log()
console.log('\x1b[30mDirectory:', path.join(dir));

server.use(static);
server.listen(PORT);


console.log('\x1b[35m\x1b[1m\nStarted in', Date.now() - t + 'ms', ' \x1b[0m');


console.log('\x1b[33m\x1b[1m\nRunning on:', '\x1b[30mhttp://localhost:' + PORT + '/', ' \x1b[0m');