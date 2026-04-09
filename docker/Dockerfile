# Stage 1 — builder (install dependencies, compile anything needed)
FROM python:3.11-slim AS builder
WORKDIR /build
# use virtual environment to clear cache
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2 — final image (copy only what's needed to run)
FROM python:3.11-slim AS runtime
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Copy only your application code
COPY src/ ./src/

# Non-root user — security best practice
RUN useradd -m appuser
USER appuser

CMD ["python", "src/etl.py"]