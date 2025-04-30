## Framewrok for RAG (FRAG)

## ⚠️ Important Note

This project is still under active development and should be considered in a pre-release state. It has not been thoroughly tested yet, and some features may be incomplete or unstable. Use it at your own discretion and report any issues or bugs.

Contributions, feedback, and suggestions are welcome as we work toward a stable release!



# RAG Framework

This repository contains a Retrieval-Augmented Generation (RAG) framework for efficient information retrieval and natural language generation. The framework supports both Ollama (running local, open-source LLMs) and OpenAI (for cloud-based LLMs like gpt-3.5-turbo, gpt-4, etc.)

## Repository Structure

```plaintext
.
├── LICENSE
├── cl-tools
│   ├── __init__.py
│   ├── chat.py
│   └── search.py
├── config
│   ├── __init__.py
│   ├── config_loader.py
│   ├── embedding_config.yaml
│   ├── embedding_config.example.yaml
│   ├── llm_config.yaml
│   └── llm_config.example.yaml
├── django-server
│   ├── manage.py
│   ├── rag_app
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── static
│   │   │   └── rag_app
│   │   │       ├── css
│   │   │       │   └── styles.css
│   │   │       └── images
│   │   │           └── frag.jpg
│   │   ├── templates
│   │   │   └── rag_app
│   │   │       ├── base.html
│   │   │       ├── chat.html
│   │   │       ├── home.html
│   │   │       └── search.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── rag_server
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── .env
├── .env_example
├── docs
│   └── diagram
│       └── RAG_Framework.svg
├── embedding
│   ├── __init__.py
│   ├── utils.py
│   └── vector_db_setup.py
├── llm
│   └── main.py
├── readme.md
├── requirement.txt
├── retrieval
│   ├── main.py
│   └── simple_query.py
└── tests
```


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

4.  **Configure your environment:**

    * Copy .env_example to .env and set your environment-specific paths:
    
    ```bash
    cp .env_example .env
    ```
    
    * Edit the .env file to set your data paths:
    
    ```bash
    # Database and file paths
    FRAG_RAW_DB=/path/to/your/actual/data
    FRAG_DB_DIRECTORY=/path/to/your/actual/database
    # files to be indexed. Only pdf and txt are supported
    FRAG_FILE_TYPES=pdf,txt
    
    # API keys
    OPENAI_API_KEY=your_openai_api_key
    ```

5.  **Configure your embedding settings:**

    * Copy the example configuration:
    
    ```bash
    cp config/embedding_config.example.yaml config/embedding_config.yaml
    ```
    
    * Edit `config/embedding_config.yaml` where you can configure the embedding model and vector database settings.

    Here's a breakdown of the editable parameters:

    * `model_name`: This specifies the pre-trained model used for creating the embedding vectors
    * `vector_db`: This defines the type of vector database to use. Currently, only `'chromaDB'` is supported
    * `collection_name`: This specifies the name of the collection within the vector database
    * `data_language`: This specifies the language of your data (e.g., "english", "french", etc.)
    * `chunk_size`: This determines the number of sentences processed together when creating the vector database

6.  **Create vector database:**

    * After setting up your configuration, run the following command to create the vector database:

    ```bash
    python embedding/vector_db_setup.py
    ```

    * This will create a Chroma vector database using the configurations you provided.

7.  **Configure the LLM:**

    * Copy the example configuration:
    
    ```bash
    cp config/llm_config.example.yaml config/llm_config.yaml
    ```
    
    * Edit `config/llm_config.yaml` to configure the large language model settings:
    
    ```yaml
    # LLM model to use with Ollama
    llm_model: "llama3:latest"
    
    # Whether to use OpenAI (true) or Ollama (false)
    use_openai: false
    
    # OpenAI model to use if use_openai is true
    openai_model: "gpt-4o"
    
    # Prompt template for the RAG system
    prompt: |
      DOCUMENTS:
      
      {data}
      
      
      QUESTION:
      {query}
      
      
      INSTRUCTIONS:
      Answer the users QUESTION using the DOCUMENTS text above.
      Keep your answer ground in the facts of the DOCUMENT.
      If the DOCUMENT doesn't contain the facts to answer the QUESTION return NO Answer found
    ```

8.  **Run the system:**

    * Once the vector database is created, you can run the chat and search functionalities using either the Django web app or the command-line tools.

    * To run the Django app:

    ```bash
    python django-server/manage.py runserver
    ```

    * This will start the Django development server, allowing you to access the web interface for chat and search (usually at `http://127.0.0.1:8000/` in your web browser).

    * To use the command-line tools:

    ```bash
    # For chat functionality
    python cl-tools/chat.py
    
    # For search functionality with 5 results
    python cl-tools/search.py --number-results 5
    ```

![RAG Framework Diagram](docs/diagram/RAG_Framework.svg)