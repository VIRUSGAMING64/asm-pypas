import React from "react"
import  Button  from "./Button.js"

export default function Saves({arr, func}){
    console.log(arr)
    return <div className="flex items-center w-full text-left">{arr.map(({name, onClick, isicon}, idx)=>{
        return <Button key={`${name}-${idx}`} text={name} onclick={()=>{
            func(name)
        }} isicon={isicon}></Button>
    })}</div>
}