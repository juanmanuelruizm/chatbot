from chatbot.config import settings


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[str]:
    """
    Divide un texto en fragmentos de tamano aproximado chunk_size
    con solapamiento para no perder contexto entre chunks.

    Si ``chunk_size`` u ``overlap`` son ``None``, se toman los valores de la
    configuración (``CHATBOT_CHUNK_SIZE`` / ``CHATBOT_CHUNK_OVERLAP``).
    """
    chunk_size = settings.chunk_size if chunk_size is None else chunk_size
    overlap = settings.chunk_overlap if overlap is None else overlap

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        # Intentar cortar en un salto de linea o espacio para no romper palabras
        if end < len(text):
            # Buscar el ultimo salto de linea dentro del rango
            newline_pos = text.rfind("\n", start, end)
            if newline_pos > start:
                end = newline_pos + 1
            else:
                # Buscar el ultimo espacio
                space_pos = text.rfind(" ", start, end)
                if space_pos > start:
                    end = space_pos + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start >= len(text):
            break

    return chunks
