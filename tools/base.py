from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict  # JSON Schema for the parameters
    function: Callable

    def to_ollama_schema(self) -> dict:
        """Convierte la tool al formato que espera Ollama."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_schemas(self) -> list[dict]:
        """Devuelve las tools en formato Ollama para pasarlas al modelo."""
        return [t.to_ollama_schema() for t in self._tools.values()]

    def execute(self, name: str, arguments: dict) -> str:
        """Ejecuta una tool por nombre con los argumentos dados."""
        tool = self._tools.get(name)
        if tool is None:
            return f"Error: tool '{name}' not found."
        try:
            result = tool.function(**arguments)
            return str(result)
        except Exception as e:
            return f"Error executing '{name}': {e}"
