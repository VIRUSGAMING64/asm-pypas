import React from "react";

export default function (site) {
    const code = `
import React from "/_server/src/react.js";
import ReactDOM from "/_server/src/react-dom.js";
import App from "/_server/sites/${site}.js";

ReactDOM.createRoot(document.querySelector('#_root')).render(React.createElement(App));
`;

    return () => <>
        <div id="_root"></div>
        <script type="module">{code}</script>
    </>
}