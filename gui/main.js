var editor = CodeMirror.fromTextArea(document.getElementById("writer"), {
    lineNumbers: true,
    mode: "go",
    theme: "dracula",
    indentUnit: 4
});

var current = 0

async function submitCode(path) {
    
    if (current == "" && editor.getValue() == "")
        return
    
    if (current == ""){
        NewCode()
        return
    }

    var text = encodeURI(editor.getValue())
    console.log(text)
    
    var url = "/" + path + '?name=' + current + '&code=' + text;
    data = await fetch(url)
    data = await data.json()
    if (path == "run") {
        elem = document.querySelector(".output")
        console.log(elem)
        elem.innerText = data["result"]
        document.querySelector(".output").innerText = ""
        for (var i = 0; i < data["Errors"].length; i += 1) {
            var div = document.createElement("div")
            div.innerText = data["Errors"][i]
            console.log(div.innerText)
            document.querySelector(".output").appendChild(div)
        }
        
    }
}

async function changeto(idx){
    const response = await fetch("/getcodes?name="+idx)
    current = idx
    const data = await response.json()
    code = data["code"]
    editor.setValue(code)
}   

async function NewCode() { 
    var buttons = document.getElementById("saves")
    names = ""
    while (names == ""){
        names = prompt("Name of new file: ")
    }
    current = names
    buttons.innerHTML += '<button class="saves" onclick="changeto(\'' + names + '\')" id="'+names+'">' + names + "</button>"
    await fetch("/newcode?name="+names)
    editor.setValue("")
}

async function initSaved() {
    const response = await fetch("/initcodes")
    const data = await response.json()

    var buttons = document.getElementById("saves")
    ok = 0
    if (data["status"] == "ok"){
        for(var i = 0; i < data["names"].length; i ++){
            id = data["names"][i]
            buttons.innerHTML += '<button class="saves" onclick="changeto(\'' + id + '\')" id="' + id + '">' + id + "</button>"
            ok = 1
            current = id
        }
    }
    return ok
}

async function getCode() {
    console.log("getting code...")
    ok = await initSaved()
    
    if (ok == 0)
        await NewCode()

    const response = await fetch("/getcode?name=" + current);
    const data = await response.json()
    console.log(data)
    if (data["status"] == "ok") {
        editor.setValue(data["code"]);
    }  
}


async function delcurr() {
    editor.setValue("")
    var div = document.getElementById(current)
    div.remove()
    submitCode("save")
    await fetch("/delcode?name="+current)
    alert("deleted file: " + current)
    current = ""

}


getCode()

setInterval(() => {
    submitCode("save")
}, 1000);


