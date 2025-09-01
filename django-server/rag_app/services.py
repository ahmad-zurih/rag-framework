import json
import gc
from typing import Generator, Dict, Any, List
from retrieval.main import ChromaRetriever
from llm.main import Responder, OpenAIResponder
from config.config_loader import get_embedding_config, get_llm_config
from openai import OpenAI
import os

class ChatService:
    """
    Service class to handle chat operations including document retrieval and LLM responses.
    """
    
    def __init__(self):
        # Load configurations
        self.embedding_config = get_embedding_config()
        self.llm_config = get_llm_config()
        # Extract configuration values
        self.db_directory = os.environ.get("FRAG_DB_DIRECTORY")
        
        
        # Initialize retriever
        self.retriever = ChromaRetriever(
            embedding_model=self.embedding_config['model_name'],
            db_path=self.db_directory,
            db_collection=self.embedding_config['collection_name'],
            n_results=5
        )
        
        # Initialize OpenAI client if needed
        if self.llm_config['use_openai']:
            self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def search_documents(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for relevant documents based on query.
        """
        # Update n_results for this search
        self.retriever.n_results = n_results
        
        # Retrieve documents
        search_results = self.retriever.retrieve(query)
        
        # Format results for prompt
        formatted_result = self.retriever.format_results_for_prompt(search_results)
        
        # Extract document metadata for response
        documents = []
        if search_results and 'metadatas' in search_results and search_results['metadatas']:
            # Access the first (and only) list in the nested structure
            metadatas = search_results['metadatas'][0]
            docs = search_results['documents'][0] if search_results['documents'] else []
            distances = search_results['distances'][0] if search_results['distances'] else []
            
            for i, metadata in enumerate(metadatas):
                documents.append({
                    'file_name': metadata.get('file_name', 'Unknown'),
                    'chunk_id': metadata.get('chunk_id', f'chunk_{i}'),
                    'content': docs[i] if i < len(docs) else '',
                    'distance': distances[i] if i < len(distances) else 0
                })
    
        return {
            'formatted_data': formatted_result,
            'documents': documents,
            'raw_results': search_results
        }
    
    def generate_sync_response(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Generate a synchronous response for the given query.
        
        Args:
            query: The user's query
            n_results: Number of documents to retrieve
            
        Returns:
            Dictionary containing response and source documents
        """
        # Search for relevant documents
        search_data = self.search_documents(query, n_results)
        
        # Generate response using LLM
        if self.llm_config['use_openai']:
            responder = OpenAIResponder(
                data=search_data['formatted_data'],
                model=self.llm_config['openai_model'],
                prompt_template=self.llm_config['prompt'],
                query=query,
                client=self.openai_client
            )
        else:
            responder = Responder(
                data=search_data['formatted_data'],
                model=self.llm_config['llm_model'],
                prompt_template=self.llm_config['prompt'],
                query=query
            )
        
        # Get the response
        response_text = responder.generate_response()
        
        return {
            'response': response_text,
            'documents': search_data['documents'],
            'query': query,
            'model_used': self.llm_config['openai_model'] if self.llm_config['use_openai'] else self.llm_config['llm_model']
        }
    
    def generate_stream_response(self, query: str, n_results: int = 5) -> Generator[str, None, None]:
        """
        Generate a streaming response for the given query.
        
        Args:
            query: The user's query
            n_results: Number of documents to retrieve
            
        Yields:
            String chunks of the response, followed by document metadata
        """
        try:
            # Search for relevant documents
            search_data = self.search_documents(query, n_results)
            
            # Generate streaming response using LLM
            if self.llm_config['use_openai']:
                responder = OpenAIResponder(
                    data=search_data['formatted_data'],
                    model=self.llm_config['openai_model'],
                    prompt_template=self.llm_config['prompt'],
                    query=query,
                    client=self.openai_client
                )
                
                # Stream response chunks
                for chunk in responder.stream_response_chunks():
                    yield chunk
                    # Force garbage collection periodically
                    gc.collect()
            else:
                responder = Responder(
                    data=search_data['formatted_data'],
                    model=self.self.llm_config['llm_model'],
                    prompt_template=self.llm_config['prompt'],
                    query=query
                )
                
                # Stream response chunks
                chunk_count = 0
                for chunk in responder.stream_response_chunks():
                    chunk_count += 1
                    yield chunk
                    # Force garbage collection every 50 chunks
                    if chunk_count % 50 == 0:
                        gc.collect()
            
            # After streaming is complete, send document metadata
            docs_json = json.dumps(search_data['documents'])
            yield f"<|DOCS_JSON|>{docs_json}"
            
        except Exception as e:
            yield f"\n\nError during response generation: {str(e)[:100]}..."
            # Return empty documents on error
            yield "<|DOCS_JSON|>[]"
        finally:
            # Final cleanup
            gc.collect()