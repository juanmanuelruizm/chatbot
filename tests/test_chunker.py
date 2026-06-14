from chatbot.rag.chunker import chunk_text


def test_short_text_returns_single_chunk():
    text = "texto corto"
    assert chunk_text(text, chunk_size=500, overlap=100) == [text]


def test_long_text_is_split_into_multiple_chunks():
    text = "palabra " * 500  # ~4000 caracteres
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)


def test_chunks_respect_approximate_size():
    text = "x" * 2000
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    # Ningún chunk debería exceder de forma significativa el tamaño objetivo.
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_overlap_preserves_coverage():
    text = "abcdefghij " * 100
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    # El texto reconstruido sin solapamientos debe cubrir todo el contenido.
    assert "".join(chunks).count("abcdefghij") >= text.count("abcdefghij")


def test_uses_config_defaults_when_args_omitted():
    # No debe lanzar y debe devolver al menos un chunk usando la config.
    chunks = chunk_text("hola mundo")
    assert chunks == ["hola mundo"]
