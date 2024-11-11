import sys
import os


# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from config.embedding_config import model_name, vector_db, raw_db, db_diretory, chunk_size






