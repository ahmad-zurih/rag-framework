from openai import OpenAI
import os 
import json
from datetime import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from .services import ChatService

# Initialize the chat service
chat_service = ChatService()

def home(request):
    return render(request, 'rag_app/home.html')

def search_view(request):
    return render(request, 'rag_app/search.html')

def chat_view(request):
    return render(request, 'rag_app/chat.html')

@csrf_exempt
@require_POST
def search_documents(request):
    """
    Handle search requests and return relevant documents.
    """
    try:
        query = request.POST.get('query', '').strip()
        number_results = int(request.POST.get('number_results', 5))
        
        if not query:
            return JsonResponse({'error': 'Query is required'}, status=400)
        
        # Use the service to search documents
        search_data = chat_service.search_documents(query, number_results)
        
        # Format response for the frontend
        response_data = {
            'query': query,
            'documents': search_data['documents'],
            'total_results': len(search_data['documents'])
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  
@require_POST
def chat_stream(request):
    """
    Handle chat requests with streaming responses.
    """
    try:
        query = request.POST.get('query', '').strip()
        
        if not query:
            return JsonResponse({'error': 'Query is required'}, status=400)
        
        # Use the service to generate streaming response
        def response_generator():
            for chunk in chat_service.generate_stream_response(query):
                yield chunk
        
        response = StreamingHttpResponse(
            response_generator(),
            content_type='text/plain'
        )
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# New API endpoint for synchronous chat
@csrf_exempt
@require_POST  
def chat_api(request):
    """
    Handle API chat requests with synchronous responses.
    """
    try:
        # Parse JSON body for API requests
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            n_results = data.get('n_results', 5)
        else:
            # Fallback to form data
            query = request.POST.get('query', '').strip()
            n_results = int(request.POST.get('n_results', 5))
        
        if not query:
            return JsonResponse({'error': 'Query is required'}, status=400)
        
        # Use the service to generate synchronous response
        result = chat_service.generate_sync_response(query, n_results)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

