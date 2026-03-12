
import sys

import ollama

from agent import agent_loop
from tools.base import ToolRegistry
from tools.file_tools import list_directory_tool, read_file_tool, write_file_tool
from tools.code_tools import run_python_tool
from tools.rag_tools import search_documents_tool
from tools.web_tools import web_search_tool

DEFAULT_MODEL = "qwen2.5:7b"


def check_ollama_connection():
    """Verifica que Ollama este corriendo y el modelo disponible."""
    try:
        ollama.list()
    except Exception:
        print("Error: no se pudo conectar con Ollama.")
        print("Asegurate de que Ollama este instalado y corriendo (ollama serve).")
        sys.exit(1)


def create_registry() -> ToolRegistry:
    """Crea el registro de tools con todas las tools disponibles."""
    registry = ToolRegistry()
    registry.register(read_file_tool)
    registry.register(write_file_tool)
    registry.register(list_directory_tool)
    registry.register(web_search_tool)
    registry.register(run_python_tool)
    registry.register(search_documents_tool)
    return registry


def main():
    model = DEFAULT_MODEL
    print(f"Agente local con Ollama — modelo: {model}")
    print("Escribe 'salir' o 'exit' para terminar.\n")

    check_ollama_connection()

    registry = create_registry()
    history: list[dict] = []

    while True:
        try:
            user_message = input("Tu: ")
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo del chat.")
            break

        if user_message.strip() == "":
            continue

        if user_message.strip().lower() in ("salir", "exit", "quit"):
            print("Saliendo del chat.")
            break

        print("Bot: ", end="")
        bot_response = agent_loop(user_message, history, registry, model)

        if bot_response:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": bot_response})


if __name__ == "__main__":
    main()
