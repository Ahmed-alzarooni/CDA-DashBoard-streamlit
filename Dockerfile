# 1) Build dependencies
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311-build:uuid-python311-20250327-003703-74 AS build-stage

WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
  && apt-get install -y python3-pip \
  && python3 -m pip install --upgrade pip \
  && python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

# 2) Runtime image
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311:uuid-python311-20250327-003703-74

WORKDIR /app
COPY --from=build-stage /app /app

EXPOSE 8080

# This is the critical part—tell Docker how to start your app:
CMD ["python3", "-m", "streamlit", "run", "MyApp.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
