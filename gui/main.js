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

    try {
        const payload = {
            name: current,
            code: editor.getValue()
        }

        let response = await fetch("/api/" + path, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        let data = await response.json()

        if (!response.ok) {
            throw new Error(data["message"] || "request failed")
        }

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
    catch (error) {
        console.error(error)
        if (path == "run") {
            document.querySelector(".output").innerText = error.message
        }
    }
}

async function changeto(idx){
    const response = await fetch("/api/getcodes?name="+idx)
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
    var butt = document.createElement("button")
    butt.className = "saves"
    butt.onclick = function () { changeto(names) }
    butt.id = names
    butt.textContent = names
    buttons.appendChild(butt)
    await fetch("/api/newcode?name="+names)
    editor.setValue("")
}

async function initSaved() {
    const response = await fetch("/api/initcodes")
    const data = await response.json()

    var buttons = document.getElementById("saves")
    ok = 0
    if (data["status"] == "ok"){
        for(var i = 0; i < data["names"].length; i ++){
            id = data["names"][i]
            var butt = document.createElement("button")
            butt.className = "saves"
            butt.onclick = function() { changeto(id) }
            butt.id = id
            butt.textContent = id
            buttons.appendChild(butt)
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

    const response = await fetch("/api/getcode?name=" + current, { "method": "POST" });
    const data = await response.json()
    console.log(data)
    if (data["status"] == "ok") {
        editor.setValue(data["code"]);
    }  
}


async function delcurr() {
    editor.setValue("")
    var div = document.getElementById(current)
    await fetch("/api/delcurr?name="+current)
    div.remove()
    alert("deleted file: " + current)
    current = ""

}


getCode()
ini = ""
setInterval(() => {
    newcod = editor.getValue()
    if (newcod != ini) { 
        ini = newcod
        submitCode("save")
    }
}, 1000);


