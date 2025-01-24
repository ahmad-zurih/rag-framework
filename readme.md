## Framewrok for RAG (FRAG)

# RAG Framework

This repository contains a Retrieval-Augmented Generation (RAG) framework for efficient information retrieval and natural language generation.

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
│   ├── embedding_config.py
│   └── llm_config.py
├── django-server
│   ├── db.sqlite3
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



![RAG Framework Diagram](docs/diagram/RAG_Framework.svg)