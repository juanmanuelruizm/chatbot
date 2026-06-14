from chatbot.tools.base import Tool, ToolRegistry


def _make_tool(name="echo"):
    return Tool(
        name=name,
        description="Echo back the message.",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
        function=lambda message: f"echo: {message}",
    )


def test_register_and_get():
    registry = ToolRegistry()
    tool = _make_tool()
    registry.register(tool)
    assert registry.get("echo") is tool
    assert registry.get("missing") is None


def test_execute_runs_function():
    registry = ToolRegistry()
    registry.register(_make_tool())
    assert registry.execute("echo", {"message": "hola"}) == "echo: hola"


def test_execute_unknown_tool_returns_error():
    registry = ToolRegistry()
    result = registry.execute("nope", {})
    assert "not found" in result


def test_execute_captures_exceptions():
    registry = ToolRegistry()
    registry.register(_make_tool())
    # Falta el argumento requerido -> la función lanza, el registro lo captura.
    result = registry.execute("echo", {})
    assert result.startswith("Error executing 'echo'")


def test_list_schemas_uses_ollama_format():
    registry = ToolRegistry()
    registry.register(_make_tool())
    schemas = registry.list_schemas()
    assert len(schemas) == 1
    schema = schemas[0]
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "echo"
    assert "parameters" in schema["function"]
