from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings

# Import configurations using the new config loader
from config.config_loader import get_embedding_config, get_llm_config
from retrieval.main import ChromaRetriever
from llm.main import Responder, OpenAIResponder

# Get configurations
embedding_config = get_embedding_config()
llm_config = get_llm_config()

# Extract embedding configuration values
model_name = embedding_config['model_name']
collection_name = embedding_config['collection_name']

# Extract LLM configuration values
llm_model = llm_config['llm_model']
prompt = llm_config['prompt']
use_openai = llm_config['use_openai']
openai_model = llm_config['openai_model']


from openai import OpenAI
import os 
# Extract DB location from environment (defined in .env file)
db_directory = os.environ.get("FRAG_DB_DIRECTORY")



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

    # Retrieval
    retriever = ChromaRetriever(
        embedding_model=model_name, 
        db_path=db_directory, 
        db_collection=collection_name, 
        n_results=5
    )
    search_results = retriever.retrieve(user_query)
    formatted_result = retriever.format_results_for_prompt(search_results)

    if use_openai:
        openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  
            )
        responder = OpenAIResponder(data=formatted_result, model=openai_model, 
                                            prompt_template=prompt, query= user_query,cleint=openai_client)
    else:
        responder = Responder(
            data=formatted_result, 
            model=llm_model, 
            prompt_template=prompt, 
            query=user_query
        )

    # Use the generator from Responder that yields chunks
    def stream_generator():
        # We just yield the chunks of text as they arrive.
        # No HTML tags added here. We'll handle formatting on the client side.
        for chunk in responder.stream_response_chunks():
            yield chunk

    return StreamingHttpResponse(
        stream_generator(), 
        content_type='text/plain'
    )
