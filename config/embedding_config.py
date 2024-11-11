# this file containst default values related to embeddings and creating vectordb
import os

model_name = "sentence-transformers/all-mpnet-base-v2"  

vector_db = "chromaDB" # Allowed Values ['chromaDB', 'FAISS']

raw_db = "/home/ahmad-unibe/gutenberg_200"  #root directory to where raw documents are stored

db_diretory = os.path.expanduser('~') + '/.db'

chunk_size = 30

tokenizer_model = "xlm-roberta-base"

documents_type = 'txt'  #valid options: 'txt', 'pdf'