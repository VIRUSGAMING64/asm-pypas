# ASM-PyPas 🚀

ASM-PyPas es un intérprete experimental con interfaz web. Combina un backend en Flask, un motor de interpretación en Python y un editor web para crear, guardar y ejecutar código.

## ✨ Resumen

- 🌐 Backend HTTP con Flask para UI y API.
- 🧠 Motor de interpretación (tokenización, estructuras y ejecución básica).
- 📝 Editor web con CodeMirror para administrar archivos en `codes/`.

## ✅ Estado Actual

Actualmente el proyecto permite:

- 📁 Crear y eliminar archivos desde la interfaz.
- 🔄 Cargar archivos existentes al abrir la app.
- 💾 Guardar cambios automáticamente.
- ▶️ Ejecutar código vía API y mostrar resultado/errores.

## 🏗️ Arquitectura

- ⚙️ `main.py`: punto de entrada del servidor.
- 🧩 `modules/interpreter`: parser, tokens, memoria y evaluación.
- 🔌 `modules/web`: rutas web, API y utilidades.
- 🛠️ `modules/generic`: helpers compartidos.
- 🖥️ `gui`: frontend estático.
- 📂 `codes`: almacenamiento de código editable.

## 🌳 Estructura Completa Del Repositorio

```text
asm-pypas/
|- .clean
|- .gitignore
|- .todo
|- README.md
|- informe.md
|- main.py
|- requirements.txt
|- codes/
|  |- perror
|- docs/
|  |- LangReference.pdf
|  |- LangReference.tex
|  |- informe.pdf
|  |- informe.tex
|- gui/
|  |- 404.html
|  |- api.html
|  |- favicon.svg
|  |- index.html
|  |- main.js
|  |- styles.css
|- modules/
|  |- __init__.py
|  |- generic/
|  |  |- utils.py
|  |- interpreter/
|  |  |- __init__.py
|  |  |- debug.py
|  |  |- Exceptions.py
|  |  |- Expression.py
|  |  |- mainhandler.py
|  |  |- memory.py
|  |  |- structures.py
|  |  |- t_statics.py
|  |  |- Tokens.py
|  |- web/
|     |- __init__.py
|     |- index.py
|     |- api/
|     |  |- endpoints.py
|     |- core/
|        |- config.py
|        |- errors.py
|        |- saver.py
|        |- utils.py
|- scripts/
|  |- clean
|  |- clean.cpp
|  |- run.sh
```

## 📋 Requisitos

- 🐍 Python 3.10 o superior.
- 📦 pip.
- ✅ Dependencia actual: `flask`.

## 🛠️ Instalación

```bash
git clone https://github.com/VIRUSGAMING64/Interpreter.git
cd Interpreter

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Ejecución

Opción 1 (directa):

```bash
python3 main.py
```

Opción 2 (script):

```bash
bash scripts/run.sh
```

Servidor:

- 🌍 http://127.0.0.1:8000
- 🌍 http://localhost:8000

## 🔄 Flujo De Uso

1. Abre la aplicación en el navegador.
2. Crea un archivo nuevo con el botón `+`.
3. Escribe código en el editor.
4. El contenido se guarda automáticamente.
5. Ejecuta con el botón Play para ver salida y errores.

## 🔗 API

Rutas principales:

- `GET /`: interfaz principal.
- `GET /api`: vista de API.
- `GET /gui/<subpath>`: recursos estáticos.
- `POST /api/run`: ejecuta código. JSON: `{ "name": string, "code": string }`.
- `POST /api/save`: guarda código. JSON: `{ "name": string, "code": string }`.
- `POST /api/getcode?name=<archivo>`: obtiene contenido de un archivo.
- `GET /api/getcodes?name=<archivo>`: obtiene contenido de un archivo.
- `GET /api/initcodes`: lista nombres disponibles en `codes/`.
- `GET /api/newcode?name=<archivo>`: crea entrada vacía.
- `GET /api/delcurr?name=<archivo>`: elimina archivo actual.

Notas técnicas:

- 🛡️ Validación de nombre de archivo para reducir riesgo de path traversal.
- 📏 Límite de payload configurado en servidor (base: 128 MB de código).

## 🧰 Scripts

- 🚀 `scripts/run.sh`: ejecuta la app con `python -OO` y luego llama a `scripts/clean`.
- 🧹 `scripts/clean`: binario de limpieza.
- 🧪 `scripts/clean.cpp`: fuente C++ del limpiador.

## 👨‍💻 Desarrollo

```bash
source .venv/bin/activate
python3 main.py
```

## 📚 Documentación

La documentación técnica estará en `docs/`.

## ⚠️ Limitaciones Actuales

- El intérprete sigue en evolución y no cubre un lenguaje completo.
- Algunas salidas siguen orientadas a depuración.
- No hay suite formal de tests automatizados en el repositorio.