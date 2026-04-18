import React from "react";
import "./main.css"
import "tailwind"
import "codemirrormin"
import "codemirrorcss"
import "codemirrormingo"
import "codemirrordracula"
import "./styles.css"
import "materialicon"

var first_time = 1
setTimeout(() => {
    init()
    first_time = 0
    return
}, 400);


class API{
    constructor(){
        this.base = "/api/"
    }

    fetchapi(url, data=NULL){
        fetch(this.base + url, data).then(
        res.json(),  (data)=> {
            return data
        })
    }

    initcodes(){
        this.fetchapi("initcodes/")
    }
    newcode(){
        this.fetchapi("newcode/")
    }
    delcode(){
        this.fetchapi("delcode/")
    }
    save(){
        this.fetchapi("save/")
    }
    run(){
        this.fetchapi("run/")
    }

};



var outputChanger;
var Current;
var api = new API()

function init(){
    console.log("inited")
    var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
        lineNumbers: true,
        mode: "go",
        theme: "dracula",
        indentUnit: 4
    });

}




function newcode(){
    var name = prompt()
    while (~name){
        name = prompt()
    }
    
    
}


function deletecurrent(){




}


function Saves(){
    return <div className="w-full text-left"></div>

}
function Run(){
    return <button className="material-icons">chevron_right</button>
}

function New(){
    return <button onClick={newcode} className="material-icons size-12">add</button>
}

function Delete(){
    return <button onClick={deletecurrent} className="material-icons size-12">delete</button>
}

function Code(){
    return <textarea id="editor"></textarea>
}

function Console(){
    var [text, getout] = React.useState("Console")
    outputChanger = getout
    return <div className="bg-black w-full h-full">{text}</div>
}

function App() {
    return <div w-fill h-full>    
                <div className="w-full flex h-10">
                    <Saves></Saves>
                    <div className="flex">
                        <New></New>
                        <Delete></Delete>
                    </div>
                </div>
                <div className="h-3/4 w-full">
                    <Code></Code>
                </div>
                <div className="flex  w-full h-full">
                    <Console></Console>
                    <div>                
                        <Run></Run>
                    </div>
                </div>
            </div>
}


export default App

