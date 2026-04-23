# ASM-PyPas 🚀

ASM-PyPas es un intérprete experimental con backend en Python y una interfaz web para crear, guardar y ejecutar código desde el navegador.

## ✨ Resumen

- 🌐 Servidor HTTP en Flask.
- 🧠 Intérprete propio (tokenización, parser y ejecución).
- 📝 Gestión de archivos de código en `codes/`.
- 🔌 API para ejecutar, guardar, listar y borrar archivos.

## 🆕 Novedades incluidas en este README

- ✅ Estructura del repositorio actualizada a lo que existe hoy.
- ✅ Se añadieron `guic/`, `docs/` y scripts recientes.
- ✅ Se incluyó `scripts/interpreter_extreme_tests.py` como validador de estrés.
- ✅ Se eliminaron referencias detalladas a librerías de JavaScript.

## ✅ Estado actual

Actualmente el proyecto permite:

- 📁 Crear, abrir y eliminar archivos de código.
- 💾 Guardar cambios.
- ▶️ Ejecutar código vía API y devolver resultado/errores.
- 🔒 Validar nombres de archivo para evitar accesos inseguros.

## 🏗️ Arquitectura

- ⚙️ `main.py`: arranque del servidor en puerto `8000`.
- 🧩 `modules/interpreter/`: núcleo del intérprete.
- 🔌 `modules/web/`: rutas, API y utilidades web.
- 🛠️ `modules/generic/`: helpers compartidos.
- 🖥️ `gui/`: fuentes de la interfaz.
- 📦 `guic/`: salida generada para servir en runtime.
- 📂 `codes/`: archivos editables por el usuario.
- 🧪 `scripts/`: ejecución, build y utilidades.

## 🌳 Estructura del repositorio

```text
asm-pypas/
├── 📄 README.md
├── 📄 Dockerfile
├── 📄 requirements.txt
├── 📄 main.py
├── 📄 build.js
├── 📁 gui/
│   ├── 📄 index.html
│   ├── 📄 index.jsx
│   ├── 📁 app/
│   └── 📁 react/
├── 📁 modules/
│   ├── 📄 __init__.py
│   ├── 📁 generic/
│   │   └── 📄 utils.py
│   ├── 📁 interpreter/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 Exceptions.py
│   │   ├── 📄 ExprParser.py
│   │   ├── 📄 Lexer.py
│   │   ├── 📄 Tokens.py
│   │   ├── 📄 builtin.py
│   │   ├── 📄 debug.py
│   │   ├── 📄 mainhandler.py
│   │   ├── 📄 memory.py
│   │   ├── 📄 statics_values.py
│   │   ├── 📄 structures.py
│   │   └── 📄 utils.py
│   └── 📁 web/
│       ├── 📄 __init__.py
│       ├── 📄 index.py
│       ├── 📁 api/
│       │   └── 📄 endpoints.py
│       └── 📁 core/
│           ├── 📄 config.py
│           ├── 📄 errors.py
│           ├── 📄 saver.py
│           └── 📄 utils.py
├── 📁 scripts/
│   ├── 📄 buildpage.sh
│   ├── 📄 run.sh
│   ├── 📄 runsample.sh
│   ├── 📄 clean.cpp
│   └── 📄 clean
```

## 📋 Requisitos

- 🐍 Python 3.10+.
- 📦 pip.
- ✅ Dependencia backend actual (`requirements.txt`): Flask.

## 🛠️ Instalación

```bash
git clone https://github.com/VIRUSGAMING64/asm-pypas.git
cd asm-pypas

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Ejecución

Opción directa:

```bash
python3 main.py
```

Opción con script:

```bash
bash scripts/run.sh
```

Servidor:

- 🌍 http://127.0.0.1:8000
- 🌍 http://localhost:8000

## 🔄 Flujo de uso

1. Abre la app en el navegador.
2. Crea o selecciona un archivo.
3. Edita el contenido.
4. Guarda y ejecuta desde la interfaz.
5. Revisa salida y errores devueltos por la API.

## 🔗 API

Endpoints principales:

- `GET /`: interfaz principal.
- `GET /api`: endpoint para referencia/archivo de API en frontend.
- `POST /api/run`: ejecuta código.
- `POST /api/save`: guarda código.
- `GET|POST /api/getcode?name=<archivo>`: obtiene contenido.
- `GET /api/initcodes`: lista entradas disponibles.
- `GET /api/newcode?name=<archivo>`: crea una entrada vacía.
- `GET /api/delcurr?name=<archivo>`: elimina una entrada.

Formato de payload para `run` y `save`:

```json
{
    "name": "archivo.c",
    "code": "..."
}
```

## 🧰 Scripts

- 🚀 `scripts/run.sh`: construye frontend generado, ejecuta `python -OO main.py` y limpia.
- 🧱 `scripts/buildpage.sh`: regenera `guic/` desde `gui/`.
- 🧪 `scripts/interpreter_extreme_tests.py`: pruebas de estrés del intérprete.
- 🧹 `scripts/clean` y `scripts/clean.cpp`: utilidad de limpieza.
- ▶️ `scripts/runsample.sh`: ejecución auxiliar de ejemplo.

## 🧪 Pruebas

- La carpeta `tests/` existe, pero está vacía actualmente.
- La validación principal de estrés está en `scripts/interpreter_extreme_tests.py`.

## 📚 Documentación

- Documentación técnica y reportes en `docs/`.
- Frontend legado disponible en `old_gui/`.

## 🤖 Uso de IA en el proyecto

La IA se utilizó como apoyo. En concreto, se empleó para:

- redactar y reorganizar partes de la documentación, incluyendo este README.
- ayudar con el tailwind de algunos elementos frontend
- ayudar a generar dockerfile
- algunas sugerencias de código (Algunas reflejadas en el nombre de commits).
- correcion de errores menores en el código (validacion de nombres en los endpoints).

## ⚠️ Limitaciones actuales

- Parte del proyecto sigue en estado experimental.
- No hay una suite automatizada unificada dentro de `tests/`.
- El lenguaje del intérprete no implementa aún todas las características de un lenguaje completo.