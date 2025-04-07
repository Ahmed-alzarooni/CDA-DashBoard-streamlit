# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code
COPY . .

# Set environment variable for the port
ENV PORT 8080

# Expose port 8080 for the container
EXPOSE 8080

# Run the Streamlit app with proper settings
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.port", "8080"]
