from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings

from retrieval.main import ChromaRetriever
from config.embedding_config import model_name, db_directory, collection_name

from llm.main import Responder, OpenAIResponder
from config.llm_config import llm_model, prompt, use_openai, openai_model, record_data
from .models import ChatLog
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
import os 
import json



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
    


def chat_page(request):
    # Renders the chat page with the form and no answers yet
    footer_class = 'footer-absolute'
    return render(request, 'rag_app/chat.html', {'footer_class': footer_class})


@csrf_exempt
@require_POST
def chat_stream(request):
    user_query = request.POST.get('query', '').strip()
    if not user_query:
        return JsonResponse({"error": "No query provided"}, status=400)

    # -- 1) Retrieve
    retriever = ChromaRetriever(
        embedding_model=model_name, 
        db_path=db_directory, 
        db_collection=collection_name, 
        n_results=5
    )
    search_results = retriever.retrieve(user_query)

    formatted_result = retriever.format_results_for_prompt(search_results)


    doc_list_for_frontend = []
    if search_results and 'documents' in search_results and 'metadatas' in search_results:
        for doc, metadata in zip(search_results['documents'][0], search_results['metadatas'][0]):
            doc_list_for_frontend.append({
                "file_name": metadata.get('file_name', 'N/A'),
                "chunk_id": metadata.get('chunk_id', 'N/A'),
                "content": doc
            })

    # -- 2) Initialize an LLM Responder
    if use_openai:
        load_dotenv(os.path.join(settings.BASE_DIR.parent, '.env'))
        openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        responder = OpenAIResponder(
            data=formatted_result,
            model=openai_model,
            prompt_template=prompt,
            query=user_query,
            cleint=openai_client
        )
    else:
        responder = Responder(
            data=formatted_result,
            model=llm_model,
            prompt_template=prompt,
            query=user_query
        )

    # -- 3) Prepare a streaming generator
    def stream_generator():
        full_response = ""
        # First yield the LLM's output
        for chunk in responder.stream_response_chunks():
            full_response += chunk
            yield chunk

        # Yield retrieved documents info to the client
        docs_json_str = json.dumps(doc_list_for_frontend)
        final_chunk = f"<|DOCS_JSON|>{docs_json_str}"
        yield final_chunk

        # Save conversation if flag is True
        if record_data:
            ChatLog.objects.create(
                user_query=user_query,
                response=full_response,
            )


        # After the model output finishes, yield one last "special" chunk
        # so the client can parse out the retrieved docs. 
        # E.g. we prefix with a known marker: "<|DOCS_JSON|>"
        docs_json_str = json.dumps(doc_list_for_frontend)
        yield f"<|DOCS_JSON|>{docs_json_str}"

    # -- 4) Return the streaming response
    return StreamingHttpResponse(
        stream_generator(), 
        content_type='text/plain'
    )

