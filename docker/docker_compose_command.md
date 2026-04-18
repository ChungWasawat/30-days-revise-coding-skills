# Wipe everything — start fresh
docker compose down -v
docker system prune -f

# Build and run
docker compose up --build

# Verify pipeline ran successfully
docker compose logs pipeline

# Check data in Postgres
docker compose exec postgres psql -U admin warehouse \
  -c "SELECT COUNT(*), MIN(id), MAX(id) FROM posts;"

# Run your analytical queries
docker compose exec postgres psql -U admin warehouse \
  -f /app/sql/analytics.sql

# Run tests
docker compose run --rm pipeline pytest tests/ -v

# Confirm it re-runs cleanly (upsert — no duplicates)
docker compose run --rm pipeline python src/pipeline.py
docker compose exec postgres psql -U admin warehouse \
  -c "SELECT COUNT(*) FROM posts;"   # should be same count