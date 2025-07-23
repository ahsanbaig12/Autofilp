from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_video():
    video = request.files.get('video')
    if not video:
        return 'No video file provided.', 400

    input_path = '/tmp/input.mp4'
    output_path = '/tmp/output.mp4'

    video.save(input_path)

    # Run the AutoFlip pipeline (adjust the command as needed)
    command = f'python pipeline.py --input_video_path={input_path} --output_video_path={output_path}'
    result = subprocess.run(command.split(), capture_output=True)

    if result.returncode != 0:
        return f'Processing failed: {result.stderr.decode()}', 500

    return send_file(output_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
