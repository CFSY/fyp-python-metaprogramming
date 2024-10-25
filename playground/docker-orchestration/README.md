# Docker Container Orchestration

A simple container orchestration experiment that demonstrates dynamic container management and inter-container communication.

The system consists of a controller service that spawns and manages multiple worker containers, establishing communication through HTTP endpoints.

## Prerequisite

1. Install Docker Desktop:
   - Download from [Docker](https://www.docker.com/products/docker-desktop/)
   - Start Docker Desktop and wait for it to initialize

## Running the Application

1. Open Terminal and navigate to the project directory

2. Run `docker compose build`

3. Run `docker compose up controller`

4. View logs 

5. Cleanup with `docker-compose down`


## Expected Behavior

When running the application:

1. The controller service will start first
2. The controller will create a Docker network if it doesn't exist
3. Worker containers will be spawned dynamically
4. The controller will attempt to communicate with each worker
5. Each successful worker communication will show a response message
6. When stopping, all spawned containers will be automatically cleaned up

Example output:
```
docker compose up controller
[+] Running 1/0
 ✔ Container docker-orchestration-controller-1  Created                                                                                                                    0.0s 
Attaching to controller-1
controller-1  | Network worker_network already exists
controller-1  | Response from worker_worker_0: {'message': 'Hello from worker worker_0', 'status': 'success'}
controller-1  | ✅ worker_worker_0 is up and responding
controller-1  | Response from worker_worker_1: {'message': 'Hello from worker worker_1', 'status': 'success'}
controller-1  | ✅ worker_worker_1 is up and responding
controller-1  | Response from worker_worker_2: {'message': 'Hello from worker worker_2', 'status': 'success'}
controller-1  | ✅ worker_worker_2 is up and responding
controller-1 exited with code 0
```
