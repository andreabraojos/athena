
# Qué es athena

Athena es un asistente personal basado en LLM creado para utilizarlo día a día en tareas repetitivas y básicas como apoyo.

# Qué objetivo tiene

Ahorrar tiempo en tareas sistemáticas y actuar como asistente personal.

# Qué me gustaría que hiciera en meses

Ser capaz de organizarme los días, viajes, recetas, rutinas de gimnasio, ayudarme a estudiar, etc.

# Requisitos

Para que funcione, se debe disponer de la versión 3.11 de Python. Además, tener el servidor Ollama instalado en el ordenador y en ejecución. Para el modelo, usaremos qwen3:8b descargable con:

```powershell
ollama pull qwen3:8b
```

## Instalación

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configuración

Athena funciona con los valores predeterminados sin configurar variables de entorno. Estas variables permiten cambiar la conexión con Ollama:

- `ATHENA_OLLAMA_URL`: dirección de la API de Ollama. Valor predeterminado: `http://localhost:11434/api/generate`.
- `ATHENA_OLLAMA_MODEL`: modelo utilizado para generar respuestas. Valor predeterminado: `qwen3:8b`.
- `ATHENA_OLLAMA_TIMEOUT`: tiempo máximo de espera, en segundos. Valor predeterminado: `120`.

Por ejemplo, en PowerShell se puede seleccionar otro modelo para la sesión actual con:

```powershell
$env:ATHENA_OLLAMA_MODEL = "otro-modelo"
```

## Ejecución

Con Ollama en ejecución y el modelo disponible, inicia Athena desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m src.main
```

Escribe `salir` para terminar la sesión.

## Pruebas

Ejecuta la suite completa desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
