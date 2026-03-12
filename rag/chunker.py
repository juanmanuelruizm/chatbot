CHUNK_SIZE = 500  # caracteres por chunk
CHUNK_OVERLAP = 100  # solapamiento entre chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Divide un texto en fragmentos de tamano aproximado chunk_size
    con solapamiento para no perder contexto entre chunks.
    """
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
