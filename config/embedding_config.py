# this file containst default values related to embeddings and creating vectordb
import os

model_name = "sentence-transformers/all-mpnet-base-v2"  

vector_db = "chromaDB" # Allowed Values ['chromaDB', 'FAISS']

collection_name = "dsl_embeddings"

raw_db = "/mnt/c/Users/ahmad/OneDrive/Desktop/dsl_data"  #root directory to where raw documents are stored

data_language = "english" #variable for the tokenizer. Supported language = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french', 'german' ,'greek' ,'italian' ,'norwegian', 'polish' ,'portuguese', 'russian' ,'slovene','spanish', 'swedish', 'turkish']

db_directory = os.path.join(os.path.expanduser('~'), '.db')  #default. Change it to where you want to store the vector DB

chunk_size = 20
