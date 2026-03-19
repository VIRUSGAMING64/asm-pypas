# 🚀 ASM-PyPas

ASM-PyPas es un proyecto en desarrollo orientado a construir un intérprete con interfaz web para un lenguaje propio. Cuando esté finalizado, permitirá escribir código desde el navegador, administrar varios archivos fuente, guardar cambios automáticamente, ejecutar programas contra el motor del intérprete y visualizar errores o resultados desde una terminal integrada. La idea del proyecto es unir un backend en Python con una interfaz sencilla para experimentar con análisis, tokenización y ejecución de código.

## ✨ Qué hará el proyecto al finalizarse

- 🖊️ Editar programas desde una interfaz web.
- 📁 Crear, abrir, guardar y eliminar archivos de código.
- ⚙️ Interpretar instrucciones del lenguaje definido en el proyecto.
- ✅ Validar la sintaxis y reportar errores encontrados.
- 🧠 Gestionar estructuras como variables, funciones y condicionales.
- 💻 Mostrar la salida de ejecución dentro de la misma interfaz.

## 🔄 Workflow del programa

De forma general, el flujo del programa funciona así:

1. 🖥️ El usuario escribe o edita código desde la interfaz web.
2. 💾 El frontend guarda automáticamente los cambios en el servidor dentro de la carpeta `codes/`.
3. ▶️ Cuando el usuario ejecuta el código, el backend recibe el contenido desde Flask.
4. 🔎 El intérprete tokeniza y analiza las instrucciones para identificar variables, funciones, condiciones y expresiones.
5. ⚠️ Si encuentra errores de sintaxis o estructura, los devuelve a la terminal visual de la interfaz.
6. 📤 Si no hay errores, el sistema entrega el resultado de la ejecución al usuario.

Este flujo conecta la interfaz ubicada en `gui/`, la lógica principal en `main.py` y el motor del intérprete distribuido dentro de `modules/`.

## 🌳 Estructura del repositorio

```text
asm-pypas/
├── main.py
├── requirements.txt
├── README.md
├── codes/
│   └── main.app
├── gui/
│   ├── index.html
│   ├── main.js
│   ├── styles.css
│   └── lib/
│       ├── tailwind.js
│       ├── codemirror/
│       │   ├── codemirror.min.css
│       │   ├── codemirror.min.js
│       │   ├── dracula.min.css
│       │   ├── go.min.js
│       │   └── python.min.js
│       └── iconfont/
│           ├── _mixins.scss
│           ├── _variables.scss
│           ├── filled.css
│           ├── filled.scss
│           ├── material-icons.css
│           ├── material-icons.scss
│           ├── outlined.css
│           ├── outlined.scss
│           ├── round.css
│           ├── round.scss
│           ├── sharp.css
│           ├── sharp.scss
│           ├── two-tone.css
│           └── two-tone.scss
├── modules/
│   ├── __init__.py
│   ├── t_statics.py
│   ├── utils.py
│   └── objects/
│       ├── __init__.py
│       ├── ast.py
│       ├── debug.py
│       ├── Executor.py
│       ├── Expression.py
│       ├── memory.py
│       ├── saver.py
│       ├── structures.py
│       └── Tokens.py
└── templates/
```

## 📥 Cómo clonar el proyecto

```bash
git clone https://github.com/VIRUSGAMING64/Interpreter.git
cd Interpreter
```

## ▶️ Cómo ejecutarlo

### 📋 Requisitos

- 🐍 Python 3
- 📦 pip

### 🛠️ Instalación y arranque

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Después de iniciar el servidor, abre tu navegador en:

```text
http://127.0.0.1:9000
```

## 📝 Notas

- 🔹 El backend está construido con Flask.
- 🔹 La interfaz usa CodeMirror para la edición de código.
- 🔹 Los archivos creados desde la interfaz se almacenan en la carpeta `codes/`.
