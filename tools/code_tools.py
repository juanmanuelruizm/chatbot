import subprocess
import sys

from tools.base import Tool

TIMEOUT_SECONDS = 10


def run_python(code: str) -> str:
    """Ejecuta codigo Python en un subprocess aislado y devuelve stdout/stderr."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
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
        return f"Error: execution timed out after {TIMEOUT_SECONDS} seconds."
    except Exception as e:
        return f"Error executing code: {e}"


run_python_tool = Tool(
    name="run_python",
    description="Execute a Python code snippet and return its stdout and stderr. The code runs in an isolated subprocess with a 10-second timeout.",
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
