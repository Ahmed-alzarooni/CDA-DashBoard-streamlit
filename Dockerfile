FROM python:3.11-slim

WORKDIR /app

# 1) Install your Python deps into this image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy your app code
COPY . .

# 3) Expose & start
EXPOSE 8080
CMD ["python3","-m","streamlit","run","MyApp.py",
     "--server.port=8080","--server.address=0.0.0.0"]
