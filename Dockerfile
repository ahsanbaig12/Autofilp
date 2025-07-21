# Start with an official MediaPipe image that has AutoFlip ready to go.
# This saves a lot of complicated setup.
FROM gcr.io/mediapipe/mediapipe:latest

# Set up a folder for our code inside the container
WORKDIR /app

# Copy our API file into the container
COPY main.py .

# Install the two extra tools we need: Flask (the web server) and Gunicorn (a professional server runner)
RUN python3 -m pip install Flask gunicorn

# Tell Google that our service will be listening on port 8080
EXPOSE 8080

# This is the final command to start our web service when the container runs.
# It's set to not time out for one hour, giving videos plenty of time to process.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "3600", "main:app"]