import chromadb
from sentence_transformers import SentenceTransformer

class ChromaRetriever:
    """
    A class for retrieving documents from a ChromaDB collection based on semantic similarity using embeddings.
    """
    def __init__(self, embedding_model: str, db_path: str, db_collection: str, n_results: int) -> None:
        self.embedding_model = embedding_model
        self.db_path = db_path
        self.db_collection = db_collection
        self.n_results = n_results
        self.model = SentenceTransformer(self.embedding_model, trust_remote_code=True)
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
        

    def format_results_for_prompt(self, results):
        """
        Formats the retrieval results into a string suitable for the Responder's prompt.

        Args:
            results: The dictionary returned by the retrieve method.

        Returns:
            A formatted string containing the retrieved data.
        """
        if not results:
            return "No relevant data found."

        formatted_data = ""
        for idx, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            chunk_id = metadata.get('chunk_id', 'N/A')
            file_name = metadata.get('file_name', 'N/A')
            formatted_data += f"Document {idx + 1}:\n"
            formatted_data += f"Document ID: {chunk_id}\n"
            formatted_data += f"File Name: {file_name}\n"
            formatted_data += f"Content:\n{doc}\n"
            formatted_data += "-" * 80 + "\n"

        return formatted_data

    
    


    