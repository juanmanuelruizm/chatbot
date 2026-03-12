import ollama

from tools.base import ToolRegistry

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools. "
    "Use tools when they help answer the user's request. "
    "Always respond in the same language the user writes in. "
    "If you don't know something and no tool can help, say so honestly. "
    "When you use a tool, explain briefly what you did and share the result."
)

MAX_TOOL_ROUNDS = 10  # Limite de iteraciones para evitar bucles infinitos


def build_messages(history: list[dict], user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages


def agent_loop(
    user_message: str,
    history: list[dict],
    registry: ToolRegistry,
    model: str,
) -> str:
    """
    Ejecuta el agent loop:
    1. Envia el mensaje al LLM con las tools disponibles.
    2. Si el LLM pide usar una tool → la ejecuta → alimenta el resultado → repite.
    3. Si el LLM responde con texto → lo muestra en streaming → fin del turno.

    Retorna la respuesta final del asistente.
    """
    messages = build_messages(history, user_message)
    tools = registry.list_schemas()

    for _ in range(MAX_TOOL_ROUNDS):
        response = ollama.chat(model=model, messages=messages, tools=tools)
        msg = response["message"]

        # Si el modelo quiere usar tools
        if msg.get("tool_calls"):
            # Agregamos la respuesta del asistente (con tool_calls) al historial
            messages.append(msg)

            for tool_call in msg["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = tool_call["function"]["arguments"]

                print(f"  [tool] {func_name}({func_args})")

                result = registry.execute(func_name, func_args)

                # Agregamos el resultado de la tool al historial
                messages.append({
                    "role": "tool",
                    "content": result,
                })

            # Continuamos el bucle para que el modelo procese los resultados
            continue

        # Si el modelo responde con texto, hacemos streaming de la respuesta final
        final_response = _stream_final_response(messages, model, tools)
        return final_response

    # Si se alcanza el limite de iteraciones
    return "(Se alcanzo el limite de iteraciones de herramientas.)"


def _stream_final_response(
    messages: list[dict], model: str, tools: list[dict]
) -> str:
    """Hace streaming de la respuesta final del modelo."""
    full_response = ""
    try:
        stream = ollama.chat(
            model=model, messages=messages, tools=tools, stream=True
        )
        for chunk in stream:
            # Si durante el streaming el modelo pide tool, ignoramos
            if chunk["message"].get("tool_calls"):
                continue
            token = chunk["message"].get("content", "")
            if token:
                print(token, end="", flush=True)
                full_response += token
        print()
    except ollama.ResponseError as e:
        print(f"\nError del modelo: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")
    return full_response
