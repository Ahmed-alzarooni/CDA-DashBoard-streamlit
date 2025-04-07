# Build dependencies
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311-build:uuid-python311-build AS build-stage
WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y python3-pip \
 && python3 -m pip install --upgrade pip \
 && python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime image
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311:uuid-python311-runtime
WORKDIR /app
COPY --from=build-stage /app /app
EXPOSE 8080

# **This is critical**—tell the container how to start:
CMD ["python3", "-m", "streamlit", "run", "MyApp.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
