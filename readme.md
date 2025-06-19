## Framewrok for RAG (FRAG)

## ⚠️ Important Note

This project is still under active development and should be considered in a pre-release state. It has not been thoroughly tested yet, and some features may be incomplete or unstable. Use it at your own discretion and report any issues or bugs.

Contributions, feedback, and suggestions are welcome as we work toward a stable release!



# RAG Framework

This repository contains a Retrieval-Augmented Generation (RAG) framework for efficient information retrieval and natural language generation. The framework supports both Ollama (running local, open-source LLMs) and OpenAI (for cloud-based LLMs like gpt-3.5-turbo, gpt-4, etc.)


## How to Get Started


**Prerequisites:**

*   Ollama server. Install from [https://ollama.com/](https://ollama.com/)
*   For using openai api, get api key and store it in .env file in the root level of the directory

**Steps:**

1.  **Create virtual environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate virtual environment:**

    ```bash
    source venv/bin/activate # For Linux/macOS
    venv\Scripts\activate # For Windows
    ```

3.  **Install packages:**

    ```bash
    pip install -r requirement.txt
    ```

4.  **Add a vector database:**

    *   Edit the file `config/embedding_config.py` where you can add the path for the data that needs to be used for the embedding vector database.

    Here's a breakdown of the editable parameters in the file:

    *   `model_name`: This specifies the pre-trained model used for creating the embedding vectors. The example shows `"Lajavaness/bilingual-embedding-large"`, but you can choose a different model name depending on your needs.
    *   `vector_db`: This defines the type of vector database to use. Currently, only `'chromaDB'` is supported.
    *   `collection_name`: This specifies the name of the collection within the vector database where the embeddings will be stored. You can choose a name that suits your project.
    *   `raw_db`: This is the root directory where your raw documents are stored. Edit this path to point to your actual data location. For example: `raw_db = "/path/to/my/data"`
    *   `data_language`: This specifies the language of your data. The file provides a list of supported languages. Choose the one that matches your data.
    *   `db_directory`: This defines the location where the vector database will be stored. By default, it's set to the user's home directory under a `.db` folder. You can change this path to a different location if needed.
    *   `chunk_size`: This determines the number of sentences processed together when creating the vector database. You can adjust this value based on your data size and hardware capabilities.

    Example `embedding_config.py` (Remember to adapt these values to your specific setup):

    ```python
    import os

    model_name = "Lajavaness/bilingual-embedding-large"  

    vector_db = "chromaDB"

    collection_name = "my_rag_collection"

    raw_db = "/path/to/my/data"  # Replace with the actual path

    data_language = "english"

    db_directory = os.path.join(os.path.expanduser('~'), '.my_rag_db')

    chunk_size = 20
    ```

5.  **Create vector database:**

    *   After setting the data paths in `embedding_config.py`, run the following command to create the vector database:

    ```bash
    python embedding/vector_db_setup.py
    ```

    *   This will create a Chroma vector database using the configurations you provided.

6.  **LLM configurations (ollama or openai):**

    *   The file `config/llm_config.py` allows you to configure the large language model (LLM) used for text generation. You can specify the LLM and potentially edit the prompts used for generating text. This config file also allows you to choose between running ollama or openai api models. You can also choose to record chat log of users with the record_data variable. Here is an example file:
    ```python
    llm_model = 'deepseek-r1:1.5b' # select any model available on the ollama site https://ollama.com/search

    use_openai = False # set to True if using openai api and then select 'openai_model' variable

    openai_model = 'gpt-4o' # if using openai api then select which model to use

    prompt = """
    DOCUMENTS: \n
    {data}
    \n
    \n
    QUESTION:
    {query}
    \n
    \n
    INSTRUCTIONS:
    Answer the users QUESTION using the DOCUMENTS text above.
    Keep your answer ground in the facts of the DOCUMENT.
    If the DOCUMENT doesn’t contain the facts to answer the QUESTION return NO Answer found
    """

    record_data = False # set to true to record chat log
    ```

7.  **Run the system:**

    *   Once the vector database is created, you can run the chat and search functionalities using either the Django web app or the command-line tools.

    *   To run the Django app:

    ```bash
    python django-server/manage.py runserver
    ```

    *   This will start the Django development server, allowing you to access the web interface for chat and search (usually at `http://127.0.0.1:8000/` in your web browser).

    *   To use the command-line tools:

    *   The functionalities are likely defined in the `cl-tools` directory (chat.py and search.py). You can refer to those files to understand how to use the command-line interface for chat and search.

![RAG Framework Diagram](docs/diagram/RAG_Framework.svg)