# executor/views.py
from django.http import StreamingHttpResponse
from .utils.docker_runner import execute_in_container,get_docker_client
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def execute_docker(request):
    code = request.POST.get('code', '')
     # Test Docker connection first
    docker_client = get_docker_client()
    docker_client.ping()
    
    if not code.strip():
        return StreamingHttpResponse(
            "Error: No code provided\n",
            content_type='text/plain'
        )
    
    def stream_output():
        try:
            for output in execute_in_container(code):
                yield output
            yield "\nExecution completed\n"
        except Exception as e:
            yield f"\nError: {str(e)}\n"
    
    return StreamingHttpResponse(
        stream_output(),
        content_type='text/plain'
    )