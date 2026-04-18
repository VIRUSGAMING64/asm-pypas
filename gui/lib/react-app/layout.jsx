import React from "react";
import Site from "app/page";


export default function ({name}) {
    let App = Site(name);
    return (
        <html lang="en">
            <head>
                <meta charSet="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>React App</title>
            </head>
            <body>
                <App />
            </body>
        </html>
    )
}