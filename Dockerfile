# Use a slim Python image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir -r requirements.txt || true

# Expose port 8080 (required by Cloud Run)
ENV PORT=8080

# Run the Flask server
CMD ["python", "server.py"]
