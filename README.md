# Chatbot local con Ollama

Chatbot por consola que se ejecuta completamente en local usando [Ollama](https://ollama.com/) como backend de inferencia. No requiere conexion a internet ni APIs externas una vez descargado el modelo.

## Requisitos previos

- **Python 3.10+**
- **Ollama** instalado y corriendo en la maquina local.

### Instalar Ollama

Descarga Ollama desde [https://ollama.com/download](https://ollama.com/download) e instalalo siguiendo las instrucciones de tu sistema operativo.

Una vez instalado, asegurate de que el servicio este corriendo:

```bash
ollama serve
```

### Descargar el modelo

El chatbot usa por defecto el modelo `phi3:3.8b`. Para descargarlo:

```bash
ollama pull phi3:3.8b
```

Puedes usar cualquier otro modelo disponible en Ollama cambiando la variable `DEFAULT_MODEL` en `main.py`.

## Instalacion

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
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

Ejecuta el chatbot:

```bash
python main.py
```

Aparecera un prompt interactivo en la consola. Escribe tu mensaje y pulsa Enter para recibir la respuesta del modelo. Las respuestas se muestran en tiempo real mediante streaming.

Para salir, escribe `salir`, `exit` o `quit`, o pulsa `Ctrl+C`.

### Ejemplo de sesion

```
Chatbot local con Ollama — modelo: phi3:3.8b
Escribe 'salir' o 'exit' para terminar.

Tu: Hola, quien eres?
Bot: Soy un asistente virtual. Estoy aqui para ayudarte en lo que necesites.
Tu: Que es Python?
Bot: Python es un lenguaje de programacion de alto nivel, interpretado y de proposito general...
Tu: salir
Saliendo del chat.
```

## Funcionamiento

El chatbot funciona de la siguiente manera:

1. **Conexion con Ollama**: Al iniciar, verifica que el servicio de Ollama este corriendo. Si no lo esta, muestra un mensaje de error y termina.

2. **System prompt**: Cada conversacion incluye un prompt de sistema que define el comportamiento del asistente (idioma, tono, honestidad).

3. **Historial de conversacion**: Todos los mensajes (del usuario y del bot) se almacenan en memoria durante la sesion. Esto permite que el modelo tenga contexto de lo que se ha dicho anteriormente y pueda mantener una conversacion coherente.

4. **Streaming**: Las respuestas del modelo se muestran token a token en tiempo real, en lugar de esperar a que se genere la respuesta completa.

5. **Manejo de errores**: Si ocurre un error durante la comunicacion con el modelo, se muestra un mensaje descriptivo y el chat continua funcionando.

## Estructura del proyecto

```
chatbot/
  main.py             # Logica principal del chatbot
  requirements.txt    # Dependencias de Python
  README.md           # Este archivo
```

## Configuracion

Para cambiar el modelo, edita la constante `DEFAULT_MODEL` en `main.py`:

```python
DEFAULT_MODEL = "llama3:8b"  # o cualquier modelo disponible en Ollama
```

Para modificar el comportamiento del asistente, edita la constante `SYSTEM_PROMPT` en `main.py`.