import os, uuid, subprocess
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def run_code(request):
    code = request.data.get("code", "")
    if not code:
        return Response({"error": "No code provided"}, status=400)

    temp_dir = f"/tmp/code_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    filepath = os.path.join(temp_dir, "main.py")
   
    with open(filepath, "w") as f:
        f.write("print('Hello from Docker!')")
     # Normalize path for Docker
    docker_path = os.path.normpath(temp_dir).replace('\\', '/')
    try:
        
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{docker_path}:/code",
                "-w", "/code",
                "python:3.11",
                "python","main.py"
            ],
            capture_output=True,
            timeout=30
        )
        print(result)

        return Response({
            "stdout": result.stdout.decode(),
            "stderr": result.stderr.decode(),
        })

    except subprocess.TimeoutExpired:
        return Response({"error": "Execution timed out"}, status=408)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    finally:
        try:
            os.remove(filepath)
            os.rmdir(temp_dir)
        except:
            pass
