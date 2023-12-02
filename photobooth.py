# Import necessary libraries
from flask import Flask, request, render_template, send_file
import cv2
import io
import json
import base64
import requests
import numpy as np
import time

# Flask app setup
app = Flask(__name__)

#########   User Configurable Settings #################

stdip = 'http://127.0.0.1:7860' # Default running on localhost
image_output_path = None  # Output directory for before/after images
img_height = 512  # Image height for SD output
img_width = 512 # Image width for SD output

# Stable Diffusion key settings
sd_denoising_strength = 0.6
sd_num_steps = 100
sd_cfg_scale = 7
#########   End User Configurable Settings #################

# Function to capture a single image from the webcam
def capture_single_image():
    video_capture = cv2.VideoCapture(0)  # 0 is usually the default camera
    success, frame = video_capture.read()
    if success:
        video_capture.release()
        return frame
    else:
        video_capture.release()
        raise Exception("Failed to capture image from webcam.")

# Function to send a POST request
def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data), timeout=20.0)

# Function to get Stable Diffusion image
def get_sd_image(orig_image, prompt):
    img2img_url = stdip + '/sdapi/v1/img2img'
    retval, buffer = cv2.imencode('.png', orig_image)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    data = {
        "init_images": [encoded_image],
        "denoising_strength": sd_denoising_strength,
        "prompt": prompt,
        "steps": sd_num_steps,
        "cfg_scale": sd_cfg_scale,
        "width": img_width,
        "height": img_height,
        "restore_faces": False,
        "sampler_index": "DPM++ 2M Karras",
        "resize_mode": 1,
        "sd_vae": "Automatic"
    }
    try:
        response = submit_post(img2img_url, data)
        b64_image = response.json()['images'][0]
        decoded_image = base64.b64decode(b64_image)
        np_image = np.frombuffer(decoded_image, np.uint8)
        return cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    except Exception as ex:
        print("Error in get_sd_image:", ex)
        return None

# Flask route to render the web form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Flask route to handle the image capture and transformation
@app.route('/capture', methods=['POST'])
def capture_and_transform():
    try:
        user_prompt = request.form['prompt']
        selected_painter = request.form['painter']
        selected_painter = request.form['painter']

        full_prompt = f"{user_prompt}, inspired by the style of {selected_painter}"

        image = capture_single_image()
        transformed_image = get_sd_image(image, full_prompt)

        if transformed_image is not None:
            _, buffer = cv2.imencode('.png', transformed_image)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            return render_template('result.html', image_data=encoded_image)
        else:
            raise Exception("Failed to process image")
    except Exception as e:
        return str(e), 500

# Main execution
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
