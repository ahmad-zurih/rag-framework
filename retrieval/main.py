import chromadb
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, embedding_model: str, db_path: str, db_collection: str, n_results: int) -> None:
        self.embedding_model = embedding_model
        self.db_path = db_path
        self.db_collection = db_collection
        self.n_results = n_results
        self.model = SentenceTransformer(self.embedding_model)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_collection(name=self.db_collection)

    def retrieve(self, query: str):
        """Embeds the query and retrieves relevant documents from the collection."""
        try:
            embedded_query = self.model.encode(query)
            results = self.collection.query(
                query_embeddings=[embedded_query],
                n_results=self.n_results
            )
            return results
        except Exception as e:
            print(f"An error occurred during retrieval: {e}")
            return None

    
    


    