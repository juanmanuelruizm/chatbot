# Agente local con Ollama

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-local-black?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

Agente conversacional por consola que se ejecuta en local usando [Ollama](https://ollama.com/) como backend de inferencia. El agente puede usar herramientas (tools) de forma autónoma: leer y escribir archivos, listar directorios, buscar en internet, ejecutar código Python y consultar una base de conocimiento local (RAG).

## Requisitos previos

- **Python 3.10+**
- **Ollama** instalado y corriendo.

### Instalar Ollama

Descarga Ollama desde [https://ollama.com/download](https://ollama.com/download) e instálalo siguiendo las instrucciones de tu sistema operativo.

Una vez instalado, asegúrate de que el servicio esté corriendo:

```bash
ollama serve
```

### Descargar el modelo

El agente usa por defecto el modelo `qwen2.5:7b` (soporta tool calling nativo). Para descargarlo:

```bash
ollama pull qwen2.5:7b
```

Puedes usar otro modelo con soporte de tool calling cambiando `DEFAULT_MODEL` en `main.py`. Modelos compatibles: `qwen2.5`, `llama3.1`, `mistral`, entre otros.

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/juanmanuelruizm/chatbot.git
cd chatbot
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el agente:

```bash
python main.py
```

Escribe tu mensaje y pulsa Enter. El agente decidirá si necesita usar una herramienta o si puede responder directamente. Las respuestas finales se muestran en streaming.

Para salir, escribe `salir`, `exit` o `quit`, o pulsa `Ctrl+C`.

### Ejemplo de sesión

```
Agente local con Ollama — modelo: qwen2.5:7b
Escribe 'salir' o 'exit' para terminar.

Tu: lee el archivo requirements.txt
  [tool] read_file({'path': 'requirements.txt'})
Bot: El archivo requirements.txt contiene una única dependencia: ollama

Tu: crea un archivo test.txt con el texto "hola mundo"
  [tool] write_file({'path': 'test.txt', 'content': 'hola mundo'})
Bot: He creado el archivo test.txt con el contenido "hola mundo".

Tu: que archivos hay en el directorio actual?
  [tool] list_directory({'path': '.'})
Bot: En el directorio actual hay los siguientes archivos: main.py, agent.py, ...

Tu: que es Python?
Bot: Python es un lenguaje de programacion de alto nivel, interpretado y de proposito general...
```

## Herramientas disponibles

| Herramienta | Descripción |
|---|---|
| `read_file` | Lee el contenido de un archivo local |
| `write_file` | Escribe contenido en un archivo local |
| `list_directory` | Lista el contenido de un directorio |
| `web_search` | Busca en internet usando DuckDuckGo (devuelve título, snippet y URL) |
| `run_python` | Ejecuta código Python en un subprocess aislado con timeout de 10s |
| `search_documents` | Busca en la base de conocimiento local (RAG) los fragmentos más relevantes |

Las herramientas de archivos están restringidas al directorio de trabajo actual por seguridad. La búsqueda web requiere conexión a internet. La búsqueda de documentos requiere haber indexado documentos previamente.

## Funcionamiento

1. **Agent loop**: El agente usa un bucle iterativo. Envía el mensaje del usuario al LLM junto con las definiciones de herramientas disponibles. Si el modelo decide usar una herramienta, el agente la ejecuta y le devuelve el resultado. Este ciclo se repite hasta que el modelo genera una respuesta de texto final.

2. **Tool calling nativo**: Usa el soporte nativo de tool calling de Ollama (no prompt engineering). El modelo recibe las herramientas como JSON Schema y responde con llamadas estructuradas cuando las necesita.

3. **Historial de conversación**: Los mensajes se acumulan durante la sesión para mantener el contexto.

4. **Streaming**: Las respuestas finales se muestran token a token en tiempo real.

5. **Manejo de errores**: Verifica la conexión con Ollama al inicio. Los errores en herramientas se capturan y se informan al modelo para que pueda responder adecuadamente.

6. **RAG (Retrieval-Augmented Generation)**: El agente puede consultar una base de conocimiento local. Los documentos se dividen en fragmentos (chunks), se generan embeddings con Ollama y se almacenan en ChromaDB. Cuando el agente usa `search_documents`, busca los fragmentos más relevantes por similitud semántica.

## Estructura del proyecto

```
chatbot/
  main.py              # Entry point, CLI
  agent.py             # Agent loop
  tools/
    __init__.py
    base.py            # Tool registry (dataclass + registro)
    file_tools.py      # read_file, write_file, list_directory
    web_tools.py       # web_search
    code_tools.py      # run_python
    rag_tools.py       # search_documents
  rag/
    __init__.py
    chunker.py         # Divide documentos en fragmentos
    ingest.py          # Indexa documentos en ChromaDB
  documents/           # Carpeta para documentos del usuario
  chroma_db/           # Base de datos vectorial (generada automáticamente)
  requirements.txt
  README.md
  .gitignore
```

## Configuración

Para cambiar el modelo, edita la constante `DEFAULT_MODEL` en `main.py`:

```python
DEFAULT_MODEL = "llama3.1:8b"  # debe soportar tool calling
```

Para modificar el comportamiento del agente, edita `SYSTEM_PROMPT` en `agent.py`.

## RAG: Base de conocimiento local

Puedes hacer que el agente consulte tus propios documentos (PDFs, archivos de texto, Markdown).

### Indexar documentos

1. Coloca los archivos en la carpeta `documents/`.
2. Ejecuta el script de ingesta:

```bash
python -m rag.ingest
```

Esto leerá cada archivo, lo dividirá en fragmentos, generará embeddings con Ollama y los almacenará en una base de datos vectorial local (ChromaDB en `chroma_db/`).

### Consultar documentos

Una vez indexados, simplemente pregunta al agente sobre el contenido de tus documentos. El agente decidirá automáticamente cuándo usar `search_documents` para buscar fragmentos relevantes.

### Reindexar

Si modificas o agregas documentos, ejecuta `python -m rag.ingest` de nuevo. La base de datos se reconstruye cada vez.

### Formatos soportados

- `.pdf` — Texto extraído con pypdf (no soporta OCR para PDFs escaneados)
- `.txt` — Texto plano
- `.md` — Markdown

## Añadir nuevas herramientas

1. Crea la función Python en un archivo dentro de `tools/`.
2. Define un objeto `Tool` con nombre, descripción, parámetros (JSON Schema) y la función.
3. Registra la tool en `create_registry()` dentro de `main.py`.

Ejemplo:

```python
from tools.base import Tool

def my_tool(param: str) -> str:
    return f"resultado: {param}"

my_tool_def = Tool(
    name="my_tool",
    description="Description of what this tool does.",
    parameters={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "..."}
        },
        "required": ["param"],
    },
    function=my_tool,
)
```

## Licencia

Este proyecto está bajo la licencia MIT. Úsalo, modifícalo y distribúyelo libremente.

## Autor

**Juan Manuel Ruiz Muñoz**

- LinkedIn: [Juan Manuel Ruiz Muñoz](https://www.linkedin.com/in/juan-manuel-ruiz-mu%C3%B1oz/)
- GitHub: [@juanmanuelruizm](https://github.com/juanmanuelruizm)
