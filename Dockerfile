FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# ✅ Create models folder so Docker build never fails
RUN mkdir -p /app/models
COPY models ./models 2>/dev/null || true

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","src.service.app:app","--host","0.0.0.0","--port","8000"]
