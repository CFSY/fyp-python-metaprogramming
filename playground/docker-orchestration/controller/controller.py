import time
from typing import Optional

import docker
import requests
from docker.errors import DockerException
from docker.models.containers import Container
from docker.models.networks import Network
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class DockerController:
    def __init__(self):
        self.client = docker.from_env()
        self.network_name = "worker_network" # specified in compose.yml
        self.worker_containers: dict[str, Container] = {}

    def create_network(self) -> Network:
        """
        Creates the network as specified by self.network_name
        """
        try:
            network: Network = self.client.networks.get(self.network_name)
            print(f"Network {self.network_name} already exists")
            return network
        except docker.errors.NotFound:
            print(f"Creating network {self.network_name}")
            return self.client.networks.create(self.network_name, driver="bridge")

    def spawn_worker(self, worker_id: str) -> str:
        """
        Creates a new detached worker container
        """
        container: Container = self.client.containers.run(
            "worker:latest",
            environment={
                "WORKER_ID": worker_id
            },
            network=self.network_name,
            detach=True,
            name=f"worker_{worker_id}"
        )
        self.worker_containers[container.name] = container
        return container.name

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RequestException, ConnectionError)),
        after=lambda retry_state: print(f"Attempt {retry_state.attempt_number} failed, retrying...")
    )
    def ping_worker(self, container_name: str) -> Optional[dict]:
        """
        Attempt to ping the worker service
        Returns response data if successful, raises exception if failed
        """
        response = requests.get(f"http://{container_name}:5000/ping", timeout=5)
        response.raise_for_status()
        return response.json()

    def wait_for_container_healthy(self, container_name: str, timeout: int = 30) -> bool:
        """
        Wait for container to be running and healthy
        Returns True if container is ready, False if timeout or container stopped
        """
        container: Container = self.worker_containers[container_name]
        start_time = time.time()
        while time.time() - start_time < timeout:
            container.reload()  # Refresh container state

            # Check if container has stopped or errored
            if container.status in ['exited', 'dead']:
                print(f"Container {container.name} failed to start properly. Status: {container.status}")
                return False

            # Check if container is running
            if container.status == 'running':
                return True

            time.sleep(0.5)

        print(f"Timeout waiting for container {container.name} to be ready")
        return False

    def communicate_with_worker(self, worker_name: str) -> bool:
        """
        Establish communication with worker container
        Returns True if successful, False otherwise
        """
        try:
            if not self.wait_for_container_healthy(worker_name):
                return False

            response_data = self.ping_worker(worker_name)
            print(f"Response from {worker_name}: {response_data}")
            return True

        except Exception as e:
            print(f"Failed to communicate with {worker_name}: {str(e)}")
            return False

    def cleanup(self):
        for worker_container in self.worker_containers.values():
            worker_container.stop()
            worker_container.remove()

def main():
    controller = DockerController()

    try:
        controller.create_network()

        # Spawn workers
        workers: list[str] = []
        num_workers = 3
        for i in range(num_workers):
            worker_name = controller.spawn_worker(f"worker_{i}")
            workers.append(worker_name)

        # Check workers
        for worker_name in workers:
            if controller.communicate_with_worker(worker_name):
                print(f"✅ {worker_name} is up and responding")
            else:
                print(f"❌ {worker_name} failed to initialize properly")

    finally:
        controller.cleanup()


if __name__ == "__main__":
    main()
