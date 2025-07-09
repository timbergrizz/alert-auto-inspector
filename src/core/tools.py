from src.services.vector_db_service import VectorDBService

def search_knowledge_base(query: str) -> str:
    """Searches the knowledge base for a given query."""
    db_path = "./chroma_db"
    collection_name = "knowledge_base"
    vector_db_service = VectorDBService(db_path=db_path, collection_name=collection_name)
    results = vector_db_service.query_documents(query_texts=[query], n_results=5)

    return results['documents'][0]
