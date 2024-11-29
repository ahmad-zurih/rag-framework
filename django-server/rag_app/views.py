from django.shortcuts import render

from retrieval.main import ChromaRetriever
from config.embedding_config import model_name, db_directory, collection_name


def home(request):
    return render(request, 'rag_app/home.html')


def search(request):
    submitted = False
    formatted_results = []

    if request.method == "POST":
        query = request.POST["query"]
        n_results = int(request.POST["n_results"])
        submitted = True

        try:
            retriever = ChromaRetriever(
                embedding_model=model_name, 
                db_path=db_directory, 
                db_collection=collection_name, 
                n_results=n_results
            )
            raw_results = retriever.retrieve(query)

            # Process raw results into a template-friendly format
            documents = raw_results.get("documents", [[]])[0]
            metadatas = raw_results.get("metadatas", [[]])[0]
            distances = raw_results.get("distances", [[]])[0]

            for doc, metadata, distance in zip(documents, metadatas, distances):
                formatted_results.append({
                    "content": doc,
                    "file_name": metadata.get("file_name", "N/A"),
                    "chunk_id": metadata.get("chunk_id", "N/A"),
                    "distance": distance,
                })

        except Exception as e:
            print(f"Error during retrieval: {e}")

        return render(
            request,
            "rag_app/search.html",
            {"data": formatted_results, "submitted": submitted, "query": query, "n_results": n_results},
        )

    return render(request, "rag_app/search.html", {"data": formatted_results, "submitted": submitted})
    

