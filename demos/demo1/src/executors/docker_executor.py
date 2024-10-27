import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any

import docker
import docker.errors

from .base import BaseExecutor


class DockerExecutor(BaseExecutor):
    def __init__(self, worker_path: str):
        super().__init__(worker_path)
        self.client = docker.from_env()
        self.container = None
        self.temp_dir = tempfile.mkdtemp()
        self.image_id = None

    async def execute(self, inputs: Dict[str, Any]) -> Any:
        # Create Dockerfile
        dockerfile_content = f"""
        FROM python:3.9-slim
        WORKDIR /app
        COPY {Path(self.worker_path).name} worker.py
        CMD ["python", "worker.py"]
        """

        dockerfile_path = Path(self.temp_dir) / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)

        # Copy worker file to temp directory
        worker_dest = Path(self.temp_dir) / Path(self.worker_path).name
        worker_dest.write_text(Path(self.worker_path).read_text())

        try:
            # Build image
            image, _ = self.client.images.build(
                path=self.temp_dir,
                dockerfile=str(dockerfile_path),
                rm=True
            )
            self.image_id = image.id

            # Run container
            self.container = self.client.containers.run(
                image.id,
                environment={"TASK_INPUTS": json.dumps(inputs)},
                detach=True
            )

            # Wait for container to finish and get result
            result = None
            for log in self.container.logs(stream=True):
                result = json.loads(log.decode().strip())

            return result

        except Exception as e:
            raise Exception(f"Docker execution failed: {str(e)}")

    def cleanup(self):
        """Cleanup all resources including container, image, and temporary files"""
        try:
            # Remove container if it exists
            if self.container:
                try:
                    self.container.remove(force=True)
                except docker.errors.NotFound:
                    pass  # Container already removed
                except Exception as e:
                    print(f"Error removing container: {str(e)}")
                finally:
                    self.container = None

            # Remove image if it exists
            if self.image_id:
                try:
                    self.client.images.remove(self.image_id, force=True)
                except docker.errors.NotFound:
                    pass  # Image already removed
                except Exception as e:
                    print(f"Error removing image: {str(e)}")
                finally:
                    self.image_id = None

            # Remove temporary directory and all its contents
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"Error removing temporary directory: {str(e)}")

        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        finally:
            # Close docker client
            try:
                self.client.close()
            except:
                pass

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()
