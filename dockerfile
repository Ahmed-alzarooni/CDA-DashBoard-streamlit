# Use the custom AWS ECR image as the base for the pre-build stage
FROM 495519747063.dkr.ecr.us-east-2.amazonaws.com/awsfusionruntime-python311-build:uuid-python311-20250327-003703-74 AS pre-build-stage

# Update package lists and install pip if it's not already available.
RUN apt-get update && apt-get install -y python3-pip

# Copy your application code into the image
COPY . /app

# Set the working directory
WORKDIR /app

# Define the build stage based on the pre-build stage
FROM pre-build-stage AS build-stage

# Ensure you're in the correct directory
WORKDIR /app

# Upgrade pip and install dependencies from requirements.txt using Python's pip module
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

# Specify the default command (modify "app.py" to your application’s entry point)
CMD ["python3", "MyApp.py"]
