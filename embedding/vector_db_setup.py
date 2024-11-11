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
    db_diretory,
    chunk_size,  
    documents_type
)
from embedding.utils import (
    get_file_paths,
    read_text_file,
    read_pdf_file,
    split_text_into_sentences,
    chunk_sentences
)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=db_diretory)

def main():
    print("\n--- Embedding and Storing Documents in ChromaDB ---")
    print(f"Embedding Model: {model_name}")
    print(f"Document Type: {documents_type}")
    print(f"Chunk Size (sentences per chunk): {chunk_size}")
    print(f"Raw Data Directory: {raw_db}")
    print(f"Vector Database Directory: {db_diretory}\n")
    print(f"Vector Database is: {vector_db}\n")

    # Step 1: Load documents
    file_paths = get_file_paths(raw_db, f".{documents_type}")
    print(f"Found {len(file_paths)} {documents_type.upper()} files to process.\n")

    # Initialize embedding model
    embedding_model = SentenceTransformer(model_name)
    max_seq_length = embedding_model.max_seq_length  # Typically 512

    # Create or retrieve the collection in ChromaDB
    collection = client.get_or_create_collection("document_embeddings")

    for file_path in tqdm(file_paths, desc="Processing documents"):
        # Step 2: Read content based on file type
        if documents_type == 'txt':
            text = read_text_file(file_path)
        elif documents_type == 'pdf':
            text = read_pdf_file(file_path)
        else:
            print(f"Unsupported document type: {documents_type}")
            continue

        # Step 3: Split text into sentences
        sentences = split_text_into_sentences(text)

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

    print("\n--- Embedding and Storage Complete ---")
    print(f"Stored {len(file_paths)} documents in ChromaDB.\n")

if __name__ == "__main__":
    main()
