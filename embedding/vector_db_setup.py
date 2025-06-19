import sys
import os
import chromadb
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import configurations and utility functions
from config.embedding_config import (
    model_name,
    vector_db,
    raw_db,
    data_language,
    db_directory,
    chunk_size,
    collection_name
)
from embedding.utils import (
    get_file_paths,
    read_text_file,
    read_pdf_file,
    split_text_into_sentences,
    chunk_sentences
)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=db_directory)

def main():
    print("\n--- Embedding and Storing Documents in ChromaDB ---")
    print(f"Embedding Model: {model_name}")
    print(f"Chunk Size (sentences per chunk): {chunk_size}")
    print(f"Raw Data Directory: {raw_db}")
    print(f"Vector Database Directory: {db_directory}\n")
    print(f"Vector Database is: {vector_db}\n")

    # Step 1: Load documents (txt and pdf)
    file_paths = get_file_paths(raw_db, ["txt", "pdf"])
    print(f"Found {len(file_paths)} files to process.\n")

    # Initialize embedding model
    embedding_model = SentenceTransformer(model_name, trust_remote_code=True)
    max_seq_length = embedding_model.max_seq_length  # Typically 512 for older models. Newer ones have larger input size

    # Create or retrieve the collection in ChromaDB
    collection = client.get_or_create_collection(collection_name)

    
    total_chunks = 0

    for file_path in tqdm(file_paths, desc="Processing documents"):
        # Step 2: Read content based on file type
        if file_path.endswith('.txt'):
            text = read_text_file(file_path)
        elif file_path.endswith('.pdf'):
            text = read_pdf_file(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            continue

        # Step 3: Split text into sentences
        sentences = split_text_into_sentences(text, data_language)

        # Step 4: Chunk sentences into groups
        chunks = chunk_sentences(sentences, chunk_size)

        # Use file name as the document ID and create metadata with chunk index
        file_name = os.path.basename(file_path)
        for i, chunk_text in enumerate(chunks):
            # Step 5: Embed each chunk
            embedding = embedding_model.encode(
                chunk_text,
                truncation=True,
                max_length=max_seq_length
            )

            # Create a unique ID for each chunk
            chunk_id = f"{file_name}_chunk_{i}"
            collection.add(
                documents=[chunk_text],
                embeddings=[embedding],
                metadatas=[{"file_name": file_name, "chunk_id": i}],
                ids=[chunk_id]
            )
            total_chunks += 1

    print("\n--- Embedding and Storage Complete ---")
    print(f"Stored {len(file_paths)} documents in ChromaDB.\n")
    print(f"Stored {total_chunks} Chunks in the DB")

if __name__ == "__main__":
    main()
