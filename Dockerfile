# Start from a specific, recently patched Python slim image (Debian-based) to avoid known vulnerabilities
# choosing a fixed tag helps prevent unexpected CVEs from rolling forward
FROM python:3.11.12-slim-bullseye

# this lightweight Linux distribution (Debian slim) provides minimal attack surface

WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application
COPY app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
