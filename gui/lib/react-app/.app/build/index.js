console.log('\x1b[32m\x1b[1mBuilding...\n');
console.log(process.cwd())
var t = Date.now();

const jsx = require('../dev/server/urls/jsx');
const fs = require('fs');
const path = require('path');
const compile = require('../dev/compiler').transform;
const transform = require('../dev/compiler/jsx');
const dir = process.argv[2];

try {
    fs.rmSync(dir, { recursive: true, force: true });
} catch (error) {
    console.log(error)
}

const { SOURCES_PATH, PUBLIC_PATH, SERVER_URL, SOURCES_URL, PUBLIC_URL, APP_PATH, LAYOUT_NAME, SERVER_PATH, PAGE_NAME, PAGES_DIR } = require('../config.json');

const scan_folders = (dir) => {
    let folders = [];
    fs.readdirSync(dir).map(item => {
        item = path.join(dir, item);
        fs.statSync(item).isDirectory() ? folders.push(item, ...scan_folders(item)) : 0;
    });
    return folders;
}

const scan_files = (dir) => {
    let files = [];
    fs.readdirSync(dir).map(item => {
        item = path.join(dir, item);
        files.push(...(fs.statSync(item).isDirectory() ? scan_files(item) : fs.statSync(item).isFile() ? [item] : 0))
    });
    return files;
}
console.log(scan_folders(SOURCES_PATH))

const folders = {
    src: scan_folders(SOURCES_PATH),
    sites: scan_folders(PAGES_DIR)
}
const files = {
    src: scan_files(SOURCES_PATH),
    sites: scan_files(PAGES_DIR)
}

// main folders
console.log("\x1b[33m[1/2] Resolving paths...");
console.log("\x1b[30m");
fs.mkdirSync(dir);
fs.mkdirSync(path.join(dir, SERVER_URL));
fs.mkdirSync(path.join(dir, SERVER_URL, SOURCES_URL));

console.log(path.join(dir));
console.log(path.join(dir, SERVER_URL))
console.log(path.join(dir, SERVER_URL, SOURCES_URL));

// sources folders

folders.src.map(folder => {
    folder = folder.split('/');
    folder.splice(0, 1);
    folder = path.join(dir, SERVER_URL, SOURCES_URL, ...folder);

    
    console.log(folder);
    fs.mkdirSync(folder);

});

// build all files
console.log("\x1b[33m\n[2/2] Processing files...");
console.log("\x1b[30m");

files.src.map(file => {
    let url = file.split('/');

    url[0] = path.join(SERVER_URL, SOURCES_URL);
    url = path.join(...url).replaceAll('\\', '/');
    console.log(path.join(dir, url));

    let ext = path.extname(file).replace('.', '');

    const { code, type } = compile(fs.readFileSync(file), ext, url, { '.jsx': '.js' });

    if (type != ext) {
        let parsed = path.parse(url);
        fs.writeFileSync(path.join(dir, parsed.dir, parsed.name) + '.' + type, code);
    }
    else {
        fs.writeFileSync(path.join(dir, url), code);
    }

});


// build endpoints

// sites routes

fs.mkdirSync(path.join(dir, SERVER_URL, 'sites'));

folders.sites.map(folder => {

    folder = folder.split('/');
    folder.splice(0, 1);

    // html files
    fs.mkdirSync(path.join(dir, ...folder));

    // for apps in js
    folder = path.join(dir, SERVER_URL, 'sites', ...folder);
    fs.mkdirSync(folder);



    console.log(folder);
});

// build html endpoints

files.sites.map(file => {
    file = file.split('/');
        console.log(file)
    file.splice(0, 3);
    file = path.join(...file);
    var name = path.join(path.parse(file).dir, path.parse(file).name);
    var endp = path.parse(name).name;

    // .html
    fs.writeFileSync(path.join(dir, name + '.html'), jsx.render(path.join(APP_PATH, LAYOUT_NAME), { imports: { 'app/': path.join(SERVER_PATH, 'components/') }, default: 'jsx' }, { name: name.replaceAll('\\', '/') }));
    // .js
    fs.writeFileSync(path.join(dir, SERVER_URL, 'sites', name + '.js'), transform(fs.readFileSync(path.join(APP_PATH, PAGES_DIR, name + '.jsx'), 'utf-8'), `/_server/src/${endp}.js`))
});


// build libs

fs.writeFileSync(path.join(dir, SERVER_URL, SOURCES_URL, 'react.js'), fs.readFileSync(path.join(SERVER_PATH, '/react/react.js')));
fs.writeFileSync(path.join(dir, SERVER_URL, SOURCES_URL, 'react-dom.js'), fs.readFileSync(path.join(SERVER_PATH, '/react/react-dom.js')));

console.log(path.join(dir, 'index.html'))
console.log(path.join(dir, SERVER_URL, SOURCES_URL, 'app.js'))
console.log(path.join(dir, SERVER_URL, SOURCES_URL, 'react.js'))
console.log(path.join(dir, SERVER_URL, SOURCES_URL, 'react-dom.js'))


console.log('\x1b[35m\x1b[1m\nFinished in', Date.now() - t + 'ms', ' \x1b[0m');
