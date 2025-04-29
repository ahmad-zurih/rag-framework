import os
import sys
import argparse

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import configurations using the new config loader
from config.config_loader import get_embedding_config
from retrieval.main import ChromaRetriever

# Get the configuration
embedding_config = get_embedding_config()

# Extract configuration values
model_name = embedding_config['model_name']
collection_name = embedding_config['collection_name']

# Extract DB location from environment (defined in .env file)
db_directory = os.environ.get("FRAG_DB_DIRECTORY")

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