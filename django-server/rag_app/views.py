from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from retrieval.main import ChromaRetriever
from config.embedding_config import model_name, db_directory, collection_name

from llm.main import Responder
from config.llm_config import llm_model, prompt


def home(request):
    footer_class =  'footer-absolute'
    return render(request, 'rag_app/home.html', {'footer_class': footer_class,})


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
        footer_class = 'footer-flex' if submitted else 'footer-absolute'

        return render(
            request,
            "rag_app/search.html",
            {"data": formatted_results, "submitted": submitted, "query": query, "n_results": n_results, 'footer_class': footer_class,},
        )
    footer_class = 'footer-flex' if submitted else 'footer-absolute'

    return render(request, "rag_app/search.html", {"data": formatted_results, "submitted": submitted, 'footer_class': footer_class,})
    


@csrf_exempt
def chat(request):
    user_query = None
    answer = None

    if request.method == 'POST':
        user_query = request.POST.get('query', '').strip()
        if user_query:
            retriever = ChromaRetriever(
                embedding_model=model_name, 
                db_path=db_directory, 
                db_collection=collection_name, 
                n_results=5
            )
            search_results = retriever.retrieve(user_query)
            formatted_result = retriever.format_results_for_prompt(search_results)

            responder = Responder(
                data=formatted_result, 
                model=llm_model, 
                prompt_template=prompt, 
                query=user_query
            )
            answer = responder.generate_response()

    footer_class = 'footer-absolute' if (user_query or answer) else 'footer-absolute' #change this later
    return render(request, 'rag_app/chat.html', {'user_query': user_query, 'answer': answer, 'footer_class': footer_class})
