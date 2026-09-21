
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

## Registro de actividad

Athena guarda información técnica sobre las peticiones a Ollama en `data/athena.log`. El archivo se crea automáticamente al iniciar la aplicación y está excluido de Git.

El nivel predeterminado es `INFO`. Se registran datos técnicos como el modelo, el tiempo máximo de espera y si la petición ha finalizado, pero no se guardan los mensajes del usuario, las respuestas de Athena, la memoria ni la URL de Ollama.

Para consultar las últimas entradas en PowerShell:

```powershell
Get-Content data\athena.log -Encoding utf8
```

## Pruebas

Ejecuta la suite completa desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Comandos disponibles

| Comando | Función |
|---|---|
| `memoria` | Muestra toda la información almacenada en la memoria. |
| `recuerda clave = valor` | Guarda o actualiza el valor asociado a una clave. |
| `olvida clave` | Elimina de la memoria el valor asociado a una clave. |
| `tarea añade título` | Añade una tarea sin fecha de entrega. |
| `tarea añade título \| YYYY-MM-DD` | Añade una tarea con fecha de entrega. |
| `tareas` | Muestra todas las tareas guardadas. |
| `tarea completa id` | Marca como completada la tarea con el identificador indicado. |
| `tarea elimina id` | Elimina la tarea con el identificador indicado. |
| `pendientes` | Muestra las tareas que todavía no se han completado. |
| `hoy` | Muestra las tareas pendientes cuya fecha coincide con la fecha actual. |
| `salir` | Termina la conversación. |

Cualquier entrada que no coincida con estos comandos se envía al LLM junto con la memoria persistente.

## Demo de extremo a extremo

### Recorrido principal

Inicia Athena con Ollama disponible:

```powershell
.\.venv\Scripts\python.exe -m src.main
```

Introduce esta secuencia:

```text
recuerda persona_demo = Laura
memoria
tarea añade leer 1 capítulo para la demo | 2030-12-31
pendientes
¿Cómo se llama la persona de la demo?
tarea elimina ID_DE_LA_TAREA
olvida persona_demo
salir
```

La demo se considera correcta si:

- Athena confirma que ha guardado `persona_demo` y la memoria muestra `persona_demo: Laura`.
- La tarea aparece como pendiente con su identificador y la fecha `2030-12-31`.
- La respuesta del LLM identifica a Laura. Su redacción exacta puede variar.
- Los comandos de eliminación retiran los datos creados durante la demo. Sustituye `ID_DE_LA_TAREA` por el identificador mostrado por `pendientes`.
- El comando `salir` muestra el mensaje de despedida y termina el chat.

Si ya existen recuerdos o tareas locales, también pueden aparecer en la salida.

### Fallo controlado de Ollama

Configura temporalmente una dirección que no responda e inicia una segunda sesión:

```powershell
$env:ATHENA_OLLAMA_URL = "http://127.0.0.1:1/api/generate"
.\.venv\Scripts\python.exe -m src.main
```

Introduce:

```text
¿Cuál es la capital de Francia?
memoria
salir
```

La demo se considera correcta si Athena informa de que no puede conectarse con Ollama, el comando `memoria` sigue funcionando y `salir` termina el chat con normalidad.

Restaura la configuración predeterminada para la terminal actual:

```powershell
Remove-Item Env:ATHENA_OLLAMA_URL
```
