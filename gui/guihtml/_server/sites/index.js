import React from "/_server/src/react.js";
(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/_server/src/main.css';
        document.head.appendChild(link);})();
    ;
import "/_server/src/libs/tailwind.js";
import "/_server/src/libs/codemirror/codemirror.min.js";
(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '_server/src/libs/codemirror/codemirror.min.css';
        document.head.appendChild(link);})();
    ;
import "/_server/src/libs/codemirror/go.min.js";
(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '_server/src/libs/codemirror/dracula.min.css';
        document.head.appendChild(link);})();
    ;
(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/_server/src/styles.css';
        document.head.appendChild(link);})();
    ;
(()=>{
        if (!document.head) throw new Error("Missing head tag, necessary for import css from js");
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '_server/src/libs/iconfont/material-icons.css';
        document.head.appendChild(link);})();
    ;
var first_time = 1;
setTimeout(() => {
  init();
  first_time = 0;
  return;
}, 400);
var outputChanger;
var Current;
function init() {
  console.log("inited");
  var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    lineNumbers: true,
    mode: "go",
    theme: "dracula",
    indentUnit: 4
  });
}
function Saves() {
  return /*#__PURE__*/React.createElement("div", {
    className: "w-full text-left"
  });
}
function Run() {
  return /*#__PURE__*/React.createElement("button", {
    className: "material-icons"
  }, "chevron_right");
}
function New() {
  return /*#__PURE__*/React.createElement("button", {
    className: "material-icons size-14"
  }, "add");
}
function Delete() {
  return /*#__PURE__*/React.createElement("button", {
    className: "material-icons size-14"
  }, "delete");
}
function Code() {
  return /*#__PURE__*/React.createElement("textarea", {
    id: "editor"
  });
}
function Console() {
  var [text, getout] = React.useState("Console");
  outputChanger = getout;
  return /*#__PURE__*/React.createElement("div", {
    className: "bg-black w-full h-full"
  }, text);
}
function App() {
  return /*#__PURE__*/React.createElement("div", {
    "w-fill": true,
    "h-full": true
  }, /*#__PURE__*/React.createElement("div", {
    className: "w-full flex h-10"
  }, /*#__PURE__*/React.createElement(Saves, null), /*#__PURE__*/React.createElement("div", {
    className: "flex"
  }, /*#__PURE__*/React.createElement(New, null), /*#__PURE__*/React.createElement(Delete, null))), /*#__PURE__*/React.createElement("div", {
    className: "h-3/4 w-full"
  }, /*#__PURE__*/React.createElement(Code, null)), /*#__PURE__*/React.createElement("div", {
    className: "flex  w-full h-full"
  }, /*#__PURE__*/React.createElement(Console, null), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Run, null))));
}
export default App;