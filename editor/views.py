# executor/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import subprocess
import tempfile
import os
@csrf_exempt
@require_POST
def execute_python(request):
    code = request.POST.get('code', '')
    filename = request.POST.get('filename', 'main.py')
    
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)
    
    try:
        # Create a temporary file with the specified filename
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w+', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_path = tmp.name
            
        # Rename to requested filename for better error messages
        os.rename(tmp_path, f"{tmp_path}_{filename.replace('/', '_')}")
        tmp_path = f"{tmp_path}_{filename.replace('/', '_')}"
        
        result = subprocess.run(
            ['python', tmp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Clean up
        try:
            os.unlink(tmp_path)
        except:
            pass
            
        if result.returncode != 0:
            return JsonResponse({
                'output': result.stderr,
                'error': True
            })
        
        return JsonResponse({
            'output': result.stdout,
            'error': False
        })
        
    except subprocess.TimeoutExpired:
        return JsonResponse({
            'output': f'Error: Execution timed out (10 seconds) on {filename}',
            'error': True
        })
    except Exception as e:
        return JsonResponse({
            'output': f'Error in {filename}: {str(e)}',
            'error': True
        })