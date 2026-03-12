
import sys

import ollama

SYSTEM_PROMPT = (
    "You are a friendly and concise virtual assistant. "
    "Always respond in the same language the user writes in. "
    "If you don't know something, say so honestly."
)

DEFAULT_MODEL = "phi3:3.8b"


def check_ollama_connection():
    """Verifica que Ollama este corriendo y el modelo disponible."""
    try:
        ollama.list()
    except Exception:
        print("Error: no se pudo conectar con Ollama.")
        print("Asegurate de que Ollama este instalado y corriendo (ollama serve).")
        sys.exit(1)


def build_messages(history: list[dict], user_message: str) -> list[dict]:
    """Construye la lista de mensajes incluyendo el system prompt y el historial."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages


def chat_stream(messages: list[dict], model: str = DEFAULT_MODEL) -> str:
    """Envia los mensajes al modelo y muestra la respuesta en streaming."""
    full_response = ""
    try:
        stream = ollama.chat(model=model, messages=messages, stream=True)
        for chunk in stream:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)
            full_response += token
        print()
    except ollama.ResponseError as e:
        print(f"\nError del modelo: {e}")
        return ""
    except Exception as e:
        print(f"\nError inesperado: {e}")
        return ""
    return full_response


def main():
    model = DEFAULT_MODEL
    print(f"Chatbot local con Ollama — modelo: {model}")
    print("Escribe 'salir' o 'exit' para terminar.\n")

    check_ollama_connection()

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

        messages = build_messages(history, user_message)

        print("Bot: ", end="")
        bot_response = chat_stream(messages, model=model)

        if bot_response:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": bot_response})


if __name__ == "__main__":
    main()
