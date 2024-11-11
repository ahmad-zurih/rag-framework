import os
import pdfplumber
from transformers import AutoTokenizer


def get_file_paths(root_dir: str, file_extention: str) -> list[str]:
    """
    Retrieves a list of paths to all .txt files in the given root directory and its subdirectories.

    Args:
        root_dir (str): The root directory to search for .txt files.
        file_extention (str): the type of files to retrieve. For example "txt", "pdf"

    Returns:
        List[str]: A list of file paths to all .txt files found within the root directory and its subdirectories.
    """
    txt_file_paths = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(file_extention):
                txt_file_paths.append(os.path.join(dirpath, filename))
    
    return txt_file_paths


def read_text_file(file_path: str) -> str:
    """
    Reads the content of a text file and returns it as a single string.

    Args:
        file_path (str): The path to the .txt file to read.

    Returns:
        str: The content of the file as a single string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content


def read_pdf_file(file_path: str) -> str:
    """
    Reads the content of a PDF file and returns it as a single string.
    
    Args:
        file_path (str): The path to the PDF file to read.
    
    Returns:
        str: The content of the PDF as a single string.
    """
    text_content = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extract text from each page
            page_text = page.extract_text()
            if page_text:  # Ensure the page has text
                text_content.append(page_text)
    
    # Join all pages' text into a single string
    return "\n".join(text_content)


def tokenize_text(text: str, model_name: str) -> list[str]:
    """
    Tokenizes a given text using a specified multilingual tokenizer model, removing any special characters 
    (such as ▁ from SentencePiece) to provide clean tokens.

    Args:
        text (str): The input text to tokenize.
        model_name (str): The name of the multilingual model to use for tokenization.
                          Defaults to "xlm-roberta-base" for broad language coverage.

    Returns:
        list[str]: A list of clean tokens representing the tokenized text.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    tokens = tokenizer.tokenize(text)
    
    # Remove special characters like ▁ from tokens
    clean_tokens = [token.replace("▁", "") for token in tokens]
    
    return clean_tokens


def chunk_text(input_tokens: list[str], chunk_size: int) -> list[str]:
    """
    Splits a list of tokens into chunks based on a specified chunk size, then joins each chunk of tokens into a single string.

    Args:
        input_tokens (list[str]): A list of tokens (typically words or subwords) that represent the text to be chunked.
        chunk_size (int): The maximum number of tokens allowed per chunk.

    Returns:
        list[str]: A list of strings, where each string is a chunk containing up to `chunk_size` tokens joined together.
                   If the total number of tokens is less than or equal to `chunk_size`, returns a single chunk.
    """
    if len(input_tokens) <= chunk_size:
        return [" ".join(input_tokens)]
    
    chunks = []
    
    for i in range(0, len(input_tokens), chunk_size):
        chunk = " ".join(input_tokens[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks


    
        

    