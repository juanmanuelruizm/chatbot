from tools.base import Tool
from rag.ingest import get_collection, get_embedding

TOP_K = 5


def search_documents(query: str) -> str:
    """Busca en la base de documentos los fragmentos mas relevantes para la query."""
    try:
        collection = get_collection()
    except Exception as e:
        return f"Error accessing document database: {e}"

    if collection.count() == 0:
        return "No documents indexed yet. Run 'python -m rag.ingest' to index documents from the documents/ folder."

    try:
        query_embedding = get_embedding(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(TOP_K, collection.count()),
        )
    except Exception as e:
        return f"Error searching documents: {e}"

    if not results["documents"] or not results["documents"][0]:
        return "No relevant documents found."

    output = []
    for i, (doc, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0]), 1
    ):
        source = meta.get("source", "unknown")
        output.append(f"[{i}] (source: {source})\n{doc}")

    return "\n\n".join(output)


search_documents_tool = Tool(
    name="search_documents",
    description="Search the local knowledge base for document fragments relevant to a query. Documents must be indexed first with 'python -m rag.ingest'.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find relevant document fragments.",
            }
        },
        "required": ["query"],
    },
    function=search_documents,
)
