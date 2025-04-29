import os
import sys
from openai import OpenAI

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import configurations using the new config loader
from config.config_loader import get_embedding_config, get_llm_config
from retrieval.main import ChromaRetriever
from llm.main import Responder, OpenAIResponder

# Get configurations
embedding_config = get_embedding_config()
llm_config = get_llm_config()

# Extract embedding configuration values
model_name = embedding_config['model_name']
collection_name = embedding_config['collection_name']

# Extract LLM configuration values
llm_model = llm_config['llm_model']
prompt = llm_config['prompt']
openai_model = llm_config['openai_model']
use_openai = llm_config['use_openai']

# Extract DB location from environment (defined in .env file)
db_directory = os.environ.get("FRAG_DB_DIRECTORY")

openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  
)

def main():
    while True:
        retriever = ChromaRetriever(embedding_model=model_name, 
                                db_path=db_directory, 
                                db_collection=collection_name, 
                                n_results=5)
        
        user_query = str(input("Ask a question. Type quit to exit:  "))
        if user_query.lower() == "quit":
            break
        else:
            print("Looking the DB for relevant information .......")
            # get the data for the RAG and put it in str format
            search_results = retriever.retrieve(user_query)
            formated_result = retriever.format_results_for_prompt(search_results)

            if use_openai:
                responder = OpenAIResponder(data=formated_result, model=openai_model, 
                                            prompt_template=prompt, query= user_query,cleint=openai_client)
                responder.stream_response()
            else:
                responder = Responder(data=formated_result, model=llm_model, prompt_template=prompt, query=user_query)
                responder.stream_response()


if __name__ == "__main__":
    main()




