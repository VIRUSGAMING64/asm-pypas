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

    api.initcodes().then((data)=>{
        if (data["status"] == "ok"){
            var next = data["names"].map((name)=>({name, onClick:changeto, isicon:false}))
            Savesid = next
            if (outputChanger){
                outputChanger(next)
            }
        }        
    })

    setInterval(()=>{
        if (!Current || !editor){
            return
        }
        api.save(Current, editor.getValue()).catch(()=>{})
    }, 1000)


}
setTimeout(init, 1000)

function changeto(name) {
    api.getcode(name).then((data)=>{
        editor.setValue(data) 
        Current = name
    })
}

function Console({tex}){
    return <div className="w-full h-full">{tex}</div>
}

export default function App() {
    
    console.log("update...")
    
    var [arr, IdAdder] = React.useState([])
    var [consoleout, editcosole] = React.useState("Console")
    outputChanger = IdAdder

    function addSaveWithPrompt(){
        var name = prompt("Nombre:")
        while (name !== null && name === ""){
            name = prompt("Nombre:")
        }

        if (name === null){
            return
        }

        api.newcode(name).then((res)=>{

            var newSave = {name, onClick:changeto, isicon:false}
            var next = [...arr, newSave]
            Savesid = next
            IdAdder(next)
            Current = name
            editor.setValue("")
        })
    }

    function deletecurrent(){
        if (!Current){
            editcosole("No hay archivo seleccionado")
            return
        }

        api.delcode(Current).then((res)=>{
            if (!res || res["status"] !== "ok"){
                editcosole("No se pudo eliminar el archivo")
                return
            }

            var removedName = Current
            var next = arr.filter((item)=>item.name !== removedName)
            Savesid = next
            IdAdder(next)

            if (next.length > 0){
                Current = next[0].name
                changeto(Current)
            } else {
                Current = undefined
                if (editor){
                    editor.setValue("")
                }
            }

            editcosole("Eliminado: " + removedName)
        })
    }

    function run(){
        if (!Current){
            editcosole("No hay archivo seleccionado")
            return
        }

        api.run(Current, editor.getValue()).then((dato)=>{
            if (!dato){
                editcosole((dato && dato["message"]) ? dato["message"] : "Error al ejecutar")
                return
            }

            var mesg = dato["result"] + "\n"
            var errs = dato["Errors"] || []
            for(var i = 0 ; i < errs.length; i+=1){
                mesg += dato["Errors"][i] + "\n"
            }
            console.log(dato)
            console.log(mesg)
            editcosole(mesg)
        })
    }

    return(
    <div className="w-screen h-screen absolute">   
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
    )
}