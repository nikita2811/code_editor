import docker
import tempfile
import os
from contextlib import contextmanager

client = docker.from_env()

@contextmanager
def temp_python_file(code):
    try:
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp:
            tmp.write(code.encode('utf-8'))
            tmp.flush()
            yield tmp.name
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass

def get_docker_client():
    # Windows-specific Docker connection
    if os.name == 'nt':
        return docker.DockerClient(base_url='npipe:////./pipe/docker_engine')
    else:
        return docker.from_env()


def execute_in_container(code, container_image='python:3.9-slim'):
    with temp_python_file(code) as filepath:
        # Create container with mounted temp file
        container = client.containers.create(
            image=container_image,
            command=f"python /tmp/{os.path.basename(filepath)}",
            volumes={
                filepath: {
                    'bind': f'/tmp/{os.path.basename(filepath)}',
                    'mode': 'ro'
                }
            },
            tty=True,
            stdin_open=True,
            detach=True
        )
        
        try:
            container.start()
            # Stream logs in real-time
            for line in container.logs(stream=True, follow=True):
                yield line.decode('utf-8')
        finally:
            container.stop()
            container.remove()