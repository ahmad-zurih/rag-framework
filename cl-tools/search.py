import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from retrieval.main import ChromaRetriever, OpenAIChromaRetriever
from config.embedding_config import model_name, db_directory, collection_name, use_openai_embeddings, openai_embedding_model, openai_embedding_base_url


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Script to perform vectorDB semantic search')

    parser.add_argument(
        '--number-results',
        type=int,
        required=True,
        help='Number of results to display for a given query'
    )

    return parser

def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    if use_openai_embeddings:
            load_dotenv(os.path.join(parent_dir, '.env'))
            openai_client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
                base_url=openai_embedding_base_url
            )

            retriever = OpenAIChromaRetriever(
                openai_client=openai_client,
                embedding_model=openai_embedding_model,
                db_path=db_directory,
                db_collection=collection_name,
                n_results=args.number_results
                )
    else:    
        retriever = ChromaRetriever(embedding_model=model_name, 
                                db_path=db_directory, 
                                db_collection=collection_name, 
                                n_results=args.number_results)

    while True:
        query = str(input("Type a query to search the DB. Type 'quit' to exit:  "))

        if query.lower() == 'quit':
            break
        else:
            results = retriever.retrieve(query)


            # Print out the results
            print("\n--- Query Results ---\n")
            for idx, (doc, metadata, distance) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0])):
                print(f"Result {idx + 1}:")
                print(f"Document ID: {metadata.get('chunk_id', 'N/A')}")
                print(f"File Name: {metadata.get('file_name', 'N/A')}")
                print(f"Distance: {distance}")
                print(f"Content:\n{doc}\n")
                print("-" * 80)


if __name__ == "__main__":
    main()