import subprocess
import tempfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import docker


LANG_TO_IMAGE = {
    "python": "python:3",
    "javascript": "node",
    "php": "php",
}


client = docker.from_env()
container = client.containers.run(
    image=LANG_TO_IMAGE[language],
    command=get_run_command(language),
    volumes={f.name: {'bind': '/code', 'mode': 'ro'}},
    remove=True,
    stdout=True,
    stderr=True,
    timeout=10
)
result = container.decode('utf-8')

@api_view(["POST"])
def run_code(request):
    code = request.data.get("code")
    language = request.data.get("language")

    if language not in LANG_TO_IMAGE:
        return Response({"error": "Unsupported language"}, status=400)

    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=get_suffix(language), delete=False) as f:
            f.write(code)
            f.flush()
            client = docker.from_env()
            container = client.containers.run(
                image=LANG_TO_IMAGE[language],
                command=get_run_command(language),
                volumes={f.name: {'bind': '/code', 'mode': 'ro'}},
                remove=True,
                stdout=True,
                stderr=True,
                timeout=10
            )
            result = container.decode('utf-8')

        return Response({
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except subprocess.TimeoutExpired:
        return Response({"error": "Execution timed out"}, status=408)

def get_suffix(lang):
    return {
        "python": ".py",
        "javascript": ".js",
        "php": ".php"
    }[lang]

def get_run_command(lang):
    return {
        "python": "python /code.py",
        "javascript": "node /code.js",
        "php": "php /code.php"
    }[lang]
