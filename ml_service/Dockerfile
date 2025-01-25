FROM python:3.9-slim

WORKDIR /app

# Set pip configuration for better reliability
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_RETRIES=3

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 100 -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]