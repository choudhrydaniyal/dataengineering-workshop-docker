FROM python:3.12.1-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /pipeline

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

COPY requirements.txt .
COPY data_ingestion.py .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "data_ingestion.py"]