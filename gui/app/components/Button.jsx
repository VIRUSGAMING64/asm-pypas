import React from "react"

export default function Button({text, onclick, isicon = true}){
    return <button className={isicon ? "material-icons" : "border-gray-700 border-1 p-0.5 pl-2 pr-2 rounded-full bg-gray-900"} onClick={onclick}>
        {text}
    </button>

}
