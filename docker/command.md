# how to add variables through command !don't hard-code variables
```
# Pass env vars at runtime via docker run
docker run -e DB_HOST=localhost -e DB_PASSWORD=secret my-image

# Pass from a .env file (cleaner)
docker run --env-file .env my-image
```

# volumns -make what happened in container persistent
```
# Bind mount — map a local folder into the container
# Your local ./data/output is visible inside the container at /app/data/output
docker run -v $(pwd)/data:/app/data my-pipeline

# Named volume — Docker manages the storage location
# use inspect to see where data is stored
docker volume create pipeline_data
docker run -v pipeline_data:/app/data my-pipeline

# Read-only mount — container can read but not write
docker run -v $(pwd)/config:/app/config:ro my-pipeline

# Real pattern — input as read-only, output as writable
docker run \
  -v $(pwd)/data/raw:/app/data/raw:ro \
  -v $(pwd)/data/output:/app/data/output \
  --env-file .env \
  my-pipeline

# volume inspection
docker volume ls                        # list all volumes
docker volume inspect pipeline_data     # see where data is stored
docker volume rm pipeline_data          # delete volume
```

# network -make containers visible to other containers in the same network 
```
# Create a network
docker network create pipeline_net

# Run Postgres on that network
docker run -d \
  --name postgres_db \
  --network pipeline_net \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=warehouse \
  postgres:15

# It can now reach Postgres using the container name as hostname
docker run \
  --network pipeline_net \
  -e DB_HOST=postgres_db \      # <-- container name, not localhost
  -e DB_PASSWORD=secret \
  my-pipeline

# network inspection
docker network ls                        # list networks
# bridge — default, isolated from host (use this for container-to-container)
# host   — container shares host's network (faster but less isolated)
# none   — no network at all
```

# multi-stage builds -optimize dockerfile to be small and clean
```

```

# docker compose
```
# docker-compose.yml
version: "3.9"

services:
  # Postgres database
  postgres:
    image: postgres:15
    container_name: warehouse_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data   # persist DB data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql  # run on first start
    ports:
      - "5432:5432"              # expose to host for debugging with DBeaver
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      retries: 5

  # other service 
  pipeline:
    build: .                     # build from local Dockerfile
    container_name: etl_pipeline
    env_file: .env               # load secrets from .env
    environment:
      DB_HOST: ${DB_HOST}        # use service name as hostname
      DB_PORT: ${DB_PORT}
    volumes:
      - ./data/raw:/app/data/raw:ro
      - ./data/output:/app/data/output
    depends_on:
      postgres:
        condition: service_healthy    # wait for Postgres to be ready
    command: python src/etl.py

volumes:
  postgres_data:                 # named volume for DB persistence


# main command
docker compose up -d             # start all services in background
docker compose up --build        # rebuild images before starting
docker compose down              # stop and remove containers
docker compose down -v           # also delete volumes (wipe DB)
docker compose logs -f pipeline  # follow logs for pipeline service
docker compose ps                # see status of all services
docker compose exec postgres psql -U admin warehouse  # open psql shell, exec command is to like commands inside container
```