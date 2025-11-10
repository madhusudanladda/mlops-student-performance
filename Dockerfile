FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# ✅ Create empty folder (so app doesn't crash)
RUN mkdir -p /app/models

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","src.service.app:app","--host","0.0.0.0","--port","8000"]
