import httpx
import re
from pathlib import Path

prompt = """
Crea un microservicio completo en Python usando FastAPI que tenga:

- Rutas para crear, listar y eliminar usuarios
- Base de datos SQLite con SQLAlchemy
- Controlador, modelo, servicio y esquema de ejemplo (arquitectura limpia)
- Estructura de carpetas profesional
- Un archivo README.md
- requirements.txt
- Archivo main.py como punto de entrada
- .env con configuración base

Devuelve todos los archivos y carpetas necesarios. Para cada archivo, escribe así:

Archivo: ruta/del/archivo.py
```python
<contenido aquí>
```

Archivo: archivo.txt
```text
<contenido aquí>
```

No expliques nada. Solo devuelve archivos y contenido.
"""

output_dir = Path("outputs/microservicio_fastapi")
output_dir.mkdir(parents=True, exist_ok=True)

VALID_EXTENSIONS = [".py", ".txt", ".md", ".env", ".json", ".yaml", ".yml"]

def is_valid_filename(name: str) -> bool:
    name = name.strip().lower()
    return any(name.endswith(ext) for ext in VALID_EXTENSIONS)

def extract_files_from_response(text: str) -> dict:
    pattern = r"Archivo:\s*(.*?)\n```(?:python|text|bash)?\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    files = {}

    for filename, content in matches:
        filename = filename.strip().replace("\\", "/")

        if len(filename.split()) > 5:
            continue

        if not is_valid_filename(filename):
            continue

        path = output_dir / filename
        files[path] = content.strip()

    return files


try:
    response = httpx.get(
        "http://localhost:11434/code",
        params={"prompt": prompt},
        timeout=180.0
    )
    response.raise_for_status()
    result = response.json()
    code_response = result.get("code", "")
    files = extract_files_from_response(code_response)

    if not files:
        print("No se detectaron archivos válidos.")
    else:
        for filepath, content in files.items():
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Archivo creado: {filepath}")

except Exception as e:
    print(f"Error: {e}")