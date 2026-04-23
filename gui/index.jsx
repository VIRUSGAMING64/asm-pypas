import React from "react";
import  Button  from "./app/components/Button.js"
import Saves from "./app/components/Saves.js"
import API from "./app/api.js"

var outputChanger;
var Current;
var api = new API()
var Savesid = new Array()
var editor

function init() {
    console.log("inited")
    var tex = document.getElementById("editor")
    editor = CodeMirror.fromTextArea(tex, {
        lineNumbers: true,
        mode: "go",
        theme: "dracula",
        indentUnit: 4
    });
}
setTimeout(init, 1000)

function changeto(name) {
    Current = name
    api.getcode(name).then((data)=>{

        editor.setValue(data) //! change for mesg
    
    })
}

function deletecurrent(){

}

function Console({tex}){
    return <div className="w-full h-full">{tex}</div>
}

export default function App() {
    
    console.log("update...")
    
    var [arr, IdAdder] = React.useState([])
    var [consoleout, editcosole] = React.useState("Console")

    function addSaveWithPrompt(){
        var name = prompt("Nombre:")
        while (name !== null && name === ""){
            name = prompt("Nombre:")
        }

        if (name === null){
            return
        }

        var newSave = {name, onClick:changeto, isicon:false}
        var next = [...arr, newSave]
        Savesid = next
        IdAdder(next)
        console.log(next);
    }

    function run(){
        api.run(Current, editor.getValue()).then((dato)=>{
            var mesg = dato["result"]
            for(var i = 0 ; i < dato["Errors"].length; i+=1){
                mesg += dato["Errors"][i] + "<br/>"
            }
            console.log(dato)
            console.log(mesg)
            editcosole(mesg)
        })
    }

    return <div className="w-screen h-screen absolute">   
                <div className="w-full flex h-10">
                    <Saves arr = {arr} func={changeto} ></Saves>
                    <div className="flex items-center">
                        <Button onclick={addSaveWithPrompt} text="add"/>
                        <Button onclick={deletecurrent} text="delete"/>
                    </div>
                </div>
                <div className="h-3/4 w-full">
                    <textarea id="editor"></textarea>
                </div>
                <div className="flex p-4 rounded-lg border-gray-950 bg-gray-800 m-4  w-full h-full">
                    <Console tex={consoleout}></Console>
                    <div>                
                        <Button onclick={run} text="play_arrow"/>
                    </div>
                </div>
            </div>
}