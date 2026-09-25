import os
import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_FOLDER = os.path.join(PROJECT_ROOT, "docs")
DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")

os.makedirs(DB_PATH, exist_ok=True)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="zepto_policies")

def load_documents():
    if not os.path.exists(DOCS_FOLDER):
        raise FileNotFoundError(f"Docs folder not found: {DOCS_FOLDER}")

    documents = []
    for file_name in sorted(os.listdir(DOCS_FOLDER)):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(DOCS_FOLDER, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        documents.append({
            "id": os.path.splitext(file_name)[0],
            "text": text
        })

    return documents

def create_vector_store():
    documents = load_documents()

    if not documents:
        print(f"No .txt files found in: {DOCS_FOLDER}")
        return

    existing = collection.get()
    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    for document in documents:
        embedding = embedding_model.encode(document["text"]).tolist()
        collection.add(
            ids=[document["id"]],
            documents=[document["text"]],
            embeddings=[embedding]
        )

    print("All documents stored successfully in ChromaDB.")

def retrieve_documents(query, top_k=3):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results