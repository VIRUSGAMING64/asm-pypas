const babel = require("@babel/core")
const path  = require("path")
const fs    = require("fs")


var a_src = process.argv[2], a_dst = process.argv[3];


fs.mkdirSync(a_dst)



function compile(str){
    return babel.transform(str, {"presets": ["@babel/preset-react"]}).code
}

function dfs(src, dst){
    var elems = fs.readdirSync(src)
    for(var i = 0; i < elems.length; i++){
        elem = path.join(src,elems[i]);
        var t_dst = path.join(dst, elems[i])
        if(fs.statSync(elem).isDirectory()){
            fs.mkdirSync(t_dst)
            dfs(elem , t_dst)

        }else if(elem.endsWith(".jsx")){
            
            var data = fs.readFileSync(elem)
            t_dst    = t_dst.replace(".jsx" , ".js")
            data     = compile(data)
            fs.writeFileSync(t_dst, data)

        }else{
            var data = fs.readFileSync(elem)
            fs.writeFileSync(t_dst, data)
        }

    }
}



dfs(a_src, a_dst)