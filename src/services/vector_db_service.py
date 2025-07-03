import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class VectorDBService:
    def __init__(self, path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = None

    def get_or_create_collection(self, collection_name: str):
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )
        return self.collection

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection first.")
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query_documents(self, query_texts: List[str], n_results: int = 2) -> Dict[str, Any]:
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection first.")
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results
