import os
import pdfplumber
import nltk


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def get_file_paths(root_dir: str, file_extensions: list[str]) -> list[str]:
    """
    Retrieves a list of paths to all files with specified extensions in the given root directory and its subdirectories.

    Args:
        root_dir (str): The root directory to search for files.
        file_extensions (list[str]): A list of file extensions to retrieve. For example, ["txt", "pdf"]

    Returns:
        List[str]: A list of file paths to all matching files found within the root directory and its subdirectories.
    """
    file_paths = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(f".{ext}") for ext in file_extensions):
                file_paths.append(os.path.join(dirpath, filename))
    
    return file_paths



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


def split_text_into_sentences(text: str, language: str) -> list[str]:
    """
    Splits the given text into a list of sentences using NLTK's sentence tokenizer.

    Args:
        text (str): The input text to split into sentences.
        language (str): The language of the text for the sentence tokenizer

    Returns:
        list[str]: A list of sentences.
    """
    sentences = nltk.sent_tokenize(text, language=language)
    return sentences


def chunk_sentences(sentences: list[str], chunk_size: int) -> list[str]:
    """
    Groups a list of sentences into chunks, each containing up to `chunk_size` sentences.

    Args:
        sentences (list[str]): A list of sentences.
        chunk_size (int): The number of sentences per chunk.

    Returns:
        list[str]: A list of text chunks, each containing up to `chunk_size` sentences.
    """
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


    
        

    