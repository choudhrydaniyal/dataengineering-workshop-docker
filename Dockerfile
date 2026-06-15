FROM python:3.12.1-slim

WORKDIR /pipelines

COPY requirements.txt .
COPY scripts/pipeline.py .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "pipeline.py"]