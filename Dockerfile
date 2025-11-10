FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# ✅ Always create empty folder (prevents checksum crash)
RUN mkdir -p /app/models

# ✅ Proper copy (no redirect, no crash)
COPY models/ /app/models/

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","src.service.app:app","--host","0.0.0.0","--port","8000"]
