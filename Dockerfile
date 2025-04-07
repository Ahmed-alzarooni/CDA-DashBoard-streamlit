# 1. Base image with Python 3.11
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311-build:uuid-python311-20250327-003703-74 AS base

# 2. Install pip (if missing) and clean up apt caches
RUN apt-get update \
 && apt-get install -y python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# 4. Install Python dependencies (must include streamlit)
RUN python3 -m pip install --upgrade pip \
 && python3 -m pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app code
COPY . .

# 6. Expose the port Streamlit will run on
EXPOSE 8080

# 7. Start the app with Streamlit, binding to 0.0.0.0:8080
CMD ["python3", "-m", "streamlit", "run", "MyApp.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
