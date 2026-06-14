import subprocess
import sys

from chatbot.config import settings
from chatbot.tools.base import Tool


def run_python(code: str) -> str:
    """Ejecuta codigo Python en un subprocess aislado y devuelve stdout/stderr."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=settings.code_timeout_seconds,
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        if not output.strip():
            output = "(no output)"
        return output.strip()
    except subprocess.TimeoutExpired:
        return (
            f"Error: execution timed out after "
            f"{settings.code_timeout_seconds} seconds."
        )
    except Exception as e:
        return f"Error executing code: {e}"


run_python_tool = Tool(
    name="run_python",
    description=(
        "Execute a Python code snippet and return its stdout and stderr. "
        f"The code runs in an isolated subprocess with a "
        f"{settings.code_timeout_seconds}-second timeout."
    ),
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            }
        },
        "required": ["code"],
    },
    function=run_python,
)
