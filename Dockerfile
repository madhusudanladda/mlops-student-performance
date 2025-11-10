FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# ✅ Always create empty folder (prevents checksum crash)
RUN mkdir -p /app/models

# ✅ Safe copy: if folder missing → no error
COPY models /app/models 2>/dev/null || true

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","src.service.app:app","--host","0.0.0.0","--port","8000"]
