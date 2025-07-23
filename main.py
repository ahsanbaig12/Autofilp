import os
import subprocess
from flask import Flask, request, send_file, Response
from werkzeug.utils import secure_filename
import uuid

# This is our web application
app = Flask(__name__)

# Temporary folders to store videos during processing
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# This is the web address (URL) n8n will send the video to
@app.route('/autoflip', methods=['POST'])
def autoflip_video():
    # Check if a file was sent
    if 'file' not in request.files:
        return Response("Error: No file sent.", status=400)

    file = request.files['file']
    if file.filename == '':
        return Response("Error: Empty file sent.", status=400)

    # Create unique filenames to avoid mix-ups
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{secure_filename(file.filename)}")
    output_path = os.path.join(OUTPUT_FOLDER, f"{unique_id}_autoflipped.mp4")

    # Save the incoming video
    file.save(input_path)

    # This is the command that runs the actual AutoFlip tool
    autoflip_command = [
        'python3', '-m', 'mediapipe.examples.desktop.autoflip',
        '--input_video_path=' + input_path,
        '--output_video_path=' + output_path,
        '--aspect_ratio=9:16'  # We'll reframe for a vertical phone screen (9:16)
    ]

    print(f"Running AutoFlip command: {' '.join(autoflip_command)}")

    # Try to run the command
    try:
        subprocess.run(autoflip_command, check=True, timeout=3600)
        print("AutoFlip processing finished successfully.")
        # Send the finished video back
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print(f"An error occurred during AutoFlip processing: {e}")
        return Response("Error: AutoFlip processing failed.", status=500)

# This line is needed for Google Cloud Run to start the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))