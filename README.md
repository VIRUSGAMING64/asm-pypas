# ASM-PyPas 🚀

ASM-PyPas es un intérprete experimental con interfaz web. Combina un backend en Flask, un motor de interpretación en Python y un editor web para crear, guardar y ejecutar código.

## ✨ Resumen

- 🌐 Backend HTTP con Flask para UI y API.
- 🧠 Motor de interpretación con tokenización, parser y ejecución básica.
- 📝 Editor web con CodeMirror para administrar archivos en `codes/`.

## ✅ Estado Actual

Actualmente el proyecto permite:

- 📁 Crear, abrir y eliminar archivos desde la interfaz.
- 🔄 Cargar los archivos existentes al abrir la aplicación.
- 💾 Guardar cambios automáticamente.
- ▶️ Ejecutar código vía API y mostrar salida o errores.

## 🏗️ Arquitectura

- ⚙️ `main.py`: punto de entrada del servidor.
- 🧩 `modules/interpreter`: tokens, parser, estructuras y ejecución.
- 🔌 `modules/web`: rutas web, API y utilidades compartidas.
- 🛠️ `modules/generic`: helpers comunes.
- 🖥️ `gui`: frontend estático y documentación de API.
- 📂 `codes`: almacenamiento de archivos editables.
- 🧪 `scripts`: utilidades auxiliares para limpieza y arranque.

## 🌳 Estructura del repositorio

```text
asm-pypas/
├── Dockerfile
├── README.md
├── l.py
├── m.cpp
├── main
├── main.py
├── requirements.txt
├── codes/
├── docs/
│   ├── LangReference.tex
│   └── informe.tex
├── gui/
│   ├── favicon.svg
│   ├── html/
│   │   ├── 404.html
│   │   ├── api.html
│   │   └── index.html
│   ├── lib/
│   │   ├── google-sans.ttf
│   │   ├── tailwind.js
│   │   ├── codemirror/
│   │   └── iconfont/
│   ├── main.js
│   └── styles.css
├── modules/
│   ├── __init__.py
│   ├── generic/
│   │   └── utils.py
│   ├── interpreter/
│   │   ├── Exceptions.py
│   │   ├── Expression.py
│   │   ├── ExprParser.py
│   │   ├── Tokens.py
│   │   ├── builtin.py
│   │   ├── debug.py
│   │   ├── mainhandler.py
│   │   ├── memory.py
│   │   ├── structures.py
│   │   ├── t_statics.py
│   │   └── utils.py
│   └── web/
│       ├── __init__.py
│       ├── index.py
│       ├── api/
│       │   └── endpoints.py
│       └── core/
│           ├── config.py
│           ├── errors.py
│           ├── saver.py
│           └── utils.py
└── scripts/
	├── clean
	├── clean.cpp
	└── run.sh
```

## 📋 Requisitos

- 🐍 Python 3.10 o superior.
- 📦 pip.
- ✅ Dependencia actual: Flask.

## 🛠️ Instalación

```bash
git clone https://github.com/VIRUSGAMING64/Interpreter.git
cd Interpreter

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Ejecución

Opción 1, directa:

```bash
python3 main.py
```

Opción 2, con script:

```bash
bash scripts/run.sh
```

Servidor:

- 🌍 http://127.0.0.1:8000
- 🌍 http://localhost:8000

## 🔄 Flujo de uso

1. Abre la aplicación en el navegador.
2. Crea o selecciona un archivo.
3. Escribe código en el editor.
4. El contenido se guarda automáticamente.
5. Ejecuta con el botón Play para ver salida y errores.

## 🔗 API

Rutas disponibles:

- `GET /`: interfaz principal.
- `GET /api`: página de referencia de API.
- `GET /gui/<subpath>`: recursos estáticos del frontend.
- `POST /api/run`: ejecuta código. JSON: `{ "name": "file.asm", "code": "..." }`.
- `POST /api/save`: guarda código. JSON: `{ "name": "file.asm", "code": "..." }`.
- `GET /api/getcode?name=<archivo>`: obtiene el contenido de un archivo.
- `POST /api/getcode?name=<archivo>`: también acepta el mismo acceso para compatibilidad.
- `GET /api/initcodes`: lista los nombres disponibles en `codes/`.
- `GET /api/newcode?name=<archivo>`: crea una entrada vacía.
- `GET /api/delcurr?name=<archivo>`: elimina el archivo actual.

Respuestas y validación:

- `success`: normalmente devuelve `{"status": "ok"}` o `{"status": "ok", "code": "..."}`.
- `error`: devuelve `{"status": "fail", "message": "..."}` con el código HTTP correspondiente.
- Los nombres de archivo se validan para evitar path traversal.
- El servidor limita el payload JSON a 128 MB de código.

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

- La documentación técnica está en `docs/`.
- La referencia rápida de endpoints está en `gui/html/api.html`.

## ⚠️ Limitaciones actuales

- Algunas salidas siguen orientadas a depuración.
- Existen algunos bugs conocidos sin solucionar
- No hay suite formal de tests automatizados en el repositorio.