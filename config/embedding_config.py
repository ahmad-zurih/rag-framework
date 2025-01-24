# this file containst default values related to embeddings and creating vectordb
import os

model_name = "Lajavaness/bilingual-embedding-large"  #choose any embedding model you prefer

vector_db = "chromaDB" # Allowed Values ['chromaDB', 'FAISS']. Only ChromaDB works now

collection_name = "my_collection"

raw_db = "/path/to/data"  #root directory to where raw documents are stored

data_language = "english" #variable for the tokenizer. Supported language = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french', 'german' ,'greek' ,'italian' ,'norwegian', 'polish' ,'portuguese', 'russian' ,'slovene','spanish', 'swedish', 'turkish']

db_directory = os.path.join(os.path.expanduser('~'), '.db')  #default. Change it to where you want to store the vector DB

chunk_size = 20   #number of sentences each chunk will contain in the vector db
