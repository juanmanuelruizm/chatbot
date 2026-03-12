import os

from tools.base import Tool

# Directorio base permitido (el directorio de trabajo actual)
ALLOWED_BASE_DIR = os.path.abspath(".")


def _safe_resolve(path: str) -> str:
    """Resuelve un path y verifica que esté dentro del directorio permitido."""
    resolved = os.path.abspath(path)
    if not resolved.startswith(ALLOWED_BASE_DIR):
        raise PermissionError(
            f"Access denied: path '{path}' is outside the allowed directory."
        )
    return resolved


def read_file(path: str) -> str:
    """Lee un archivo local y devuelve su contenido."""
    safe_path = _safe_resolve(path)
    if not os.path.isfile(safe_path):
        return f"Error: file '{path}' not found."
    with open(safe_path, encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """Escribe contenido en un archivo local. Crea directorios intermedios si no existen."""
    safe_path = _safe_resolve(path)
    os.makedirs(os.path.dirname(safe_path) or ".", exist_ok=True)
    with open(safe_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File '{path}' written successfully."


def list_directory(path: str = ".") -> str:
    """Lista el contenido de un directorio."""
    safe_path = _safe_resolve(path)
    if not os.path.isdir(safe_path):
        return f"Error: directory '{path}' not found."
    entries = os.listdir(safe_path)
    if not entries:
        return "(empty directory)"
    return "\n".join(entries)


# --- Definiciones de tools para el registro ---

read_file_tool = Tool(
    name="read_file",
    description="Read the contents of a file at the given path.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative or absolute path to the file to read.",
            }
        },
        "required": ["path"],
    },
    function=read_file,
)

write_file_tool = Tool(
    name="write_file",
    description="Write content to a file at the given path. Creates the file if it doesn't exist, overwrites if it does.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative or absolute path to the file to write.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            },
        },
        "required": ["path", "content"],
    },
    function=write_file,
)

list_directory_tool = Tool(
    name="list_directory",
    description="List the contents of a directory.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the directory to list. Defaults to current directory.",
            }
        },
        "required": [],
    },
    function=list_directory,
)
