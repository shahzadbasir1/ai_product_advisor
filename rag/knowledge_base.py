from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from rag.document_processor import load_document, chunk_text


load_dotenv(override=True)

client = OpenAI()

CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "merchant_knowledge"
EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text: str) -> list[float]:
    """
    Generate an OpenAI embedding for a piece of text.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def get_collection():
    """
    Open the persistent ChromaDB collection.
    """

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )


#def index_document(file_path: str) -> int:
def index_document(
    file_path: str,
    merchant_id: str
) -> int:
    text = load_document(file_path)
    chunks = chunk_text(text)
    collection = get_collection()
    source_name = Path(file_path).name

    for index, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        collection.upsert(
            ids=[f"{merchant_id}-{source_name}-{index}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "merchant_id": merchant_id,
                    "source": source_name,
                    "chunk": index
                }
            ]
        )

    return len(chunks)

#def search_knowledge(query: str, n_results: int = 2) -> list[dict]:
def search_knowledge(
    query: str,
    merchant_id: str,
    n_results: int = 2
) -> list[dict]:
    """
    Search the merchant knowledge base for chunks
    semantically related to the query for a specific merchant.
    """

    collection = get_collection()
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "merchant_id": merchant_id
        }
    )

    matches = []

    for i in range(len(results["documents"][0])):
        matches.append(
            {
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
        )

    return matches

def list_knowledge_documents(
    merchant_id: str
) -> list[dict]:
    """
    Return the documents currently indexed in ChromaDB
    for a specific merchant.
    """

    collection = get_collection()

    results = collection.get(
        where={
            "merchant_id": merchant_id
        },
        include=["metadatas"]
    )

    documents = {}

    for metadata in results["metadatas"]:

        source = metadata.get("source")

        if not source:
            continue

        if source not in documents:
            documents[source] = {
                "document": source,
                "chunks": 0
            }

        documents[source]["chunks"] += 1

    return sorted(
        documents.values(),
        key=lambda item: item["document"].lower()
    )