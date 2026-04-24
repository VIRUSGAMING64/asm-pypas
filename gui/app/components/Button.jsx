import React from "react"

export default function Button({text, onclick, isicon = true}){
    return <button className={
        isicon ? "w-8 h-8 rounded-full cursor-pointer hover:bg-indigo-600 bg-indigo-500 flex items-center justify-center material-icons text-black/80" : "saves"
        } onClick={onclick}>
        {text}
    </button>

}
