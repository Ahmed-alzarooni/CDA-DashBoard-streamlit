# 1) Build stage (installs deps)
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 2) Runtime stage (just code + deps)
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from build → runtime
COPY --from=build /usr/local/lib/python3.11/site-packages \
     /usr/local/lib/python3.11/site-packages

# Copy your application code
COPY --from=build /app /app

EXPOSE 8080
CMD ["python3","-m","streamlit","run","MyApp.py",
     "--server.port=8080","--server.address=0.0.0.0"]
