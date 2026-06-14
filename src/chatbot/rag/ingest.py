import os
import sys

import chromadb
import ollama
from pypdf import PdfReader

from chatbot.config import settings
from chatbot.rag.chunker import chunk_text

DOCUMENTS_DIR = str(settings.documents_dir)
CHROMA_DIR = str(settings.chroma_dir)
COLLECTION_NAME = settings.collection_name
EMBEDDING_MODEL = settings.embedding_model


def extract_text(filepath: str) -> str:
    """Extrae texto de un archivo segun su extension."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext in (".txt", ".md"):
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    else:
        print(f"  Formato no soportado: {filepath}")
        return ""


def get_embedding(text: str) -> list[float]:
    """Genera un embedding usando Ollama."""
    response = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return response["embeddings"][0]


def get_collection() -> chromadb.Collection:
    """Obtiene o crea la coleccion de ChromaDB."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def ingest_documents():
    """Indexa los documentos de la carpeta ``documents/`` en ChromaDB.

    Lee cada archivo, lo divide en chunks, genera embeddings con Ollama y los
    almacena en la base de datos vectorial.
    """
    if not os.path.isdir(DOCUMENTS_DIR):
        print(f"Error: la carpeta '{DOCUMENTS_DIR}' no existe.")
        print("Creala y coloca tus documentos ahi.")
        sys.exit(1)

    files = [
        f for f in os.listdir(DOCUMENTS_DIR)
        if os.path.isfile(os.path.join(DOCUMENTS_DIR, f))
        and os.path.splitext(f)[1].lower() in (".pdf", ".txt", ".md")
    ]

    if not files:
        print(
            "No se encontraron documentos (.pdf, .txt, .md) en la carpeta "
            "documents/."
        )
        return

    collection = get_collection()

    # Limpiar coleccion existente para reindexar
    existing = collection.count()
    if existing > 0:
        print(f"Eliminando {existing} chunks anteriores...")
        collection.delete(where={"source": {"$ne": ""}})

    total_chunks = 0

    for filename in files:
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        print(f"Procesando: {filename}")

        text = extract_text(filepath)
        if not text.strip():
            print("  Sin contenido, saltando.")
            continue

        chunks = chunk_text(text)
        print(f"  {len(chunks)} chunks generados.")

        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_{i}"
            embedding = get_embedding(chunk)

            collection.upsert(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": filename, "chunk_index": i}],
            )

        total_chunks += len(chunks)

    print(
        f"\nIngesta completada: {len(files)} archivos, "
        f"{total_chunks} chunks totales."
    )


if __name__ == "__main__":
    ingest_documents()
