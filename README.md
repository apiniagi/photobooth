 * Install https://github.com/AUTOMATIC1111/stable-diffusion-webui on the machine with the beefcake GPU (backend)
   * add --listen and --api commandline args
 * Put photobooth.py, folders "static" and "templates" on the frontend machine (can be same as backend)
 * pip install -r requirements.txt to install frontend dependencies (or look in the file and install them manually)

# Overview
The Virtual Painting Photobooth is a Flask web application that allows users to transform their images using a Stable Diffusion model with artistic styles inspired by famous painters. The application provides an interface for capturing images using a webcam and applying chosen artistic styles to the images.

For convenience, it can be split into a *backend* machine (running the Stable Diffusion part via the powerful GPU) and a lighter *frontend* machine (running just the webcam and display) over the LAN.

 The project was inspired by drmn4ea's Haunted Mirror project https://github.com/drmn4ea/hauntedmirror.

# Features
Image Capture: Users can capture images using their webcam.
Style Selection: Users can select from various painter styles to apply to their images.
Image Transformation: The application uses the Stable Diffusion model to transform the captured images according to the selected style.
Image Display: Transformed images are displayed within a styled frame, mimicking a painting in a gallery.
Download and Print Options: Users can download or print the transformed image.

# Usage
Enter your Promt: add promt; if you want add something to result.
Select Style: Choose an artistic style from the dropdown menu.
Capture and Transform Image: Click on the "Capture and Transform Image" button to capture an image using the webcam.
View Result: The transformed image is displayed within a picture frame on the screen.
Download/Print: Use the provided buttons to download or print the image.
Navigate Back: Click the "Back" button to return to the main page and capture a new image.

# stable-diffusion-webui setup
See the https://github.com/AUTOMATIC1111/stable-diffusion-webui README for detailed instructions. A supported GPU with at least 4GB of RAM is recommended. 

You will need to add the --api commandline argument. If you will be running a separate frontend over a network, the --listen parameter must be added too. If running under Windows, add these (plus any memory options or other needed tweaks) to the 'set COMMANDLINE_ARGS=' line in webui-user.bat.

It is recommended to run the browser-based UI at least once to choose an initial model (install more if desired) and make sure everything is working. The model 'v1-5-pruned-emaonly.safetensor' produced good results for me. I installed also extension controlnet. It can be found in UI -> Extensions -> install from URL -> sd-webui-controlnet. I added an IP adapter to it to better recognize and change the face in the photo. Files from IP-Adapter https://huggingface.co/h94/IP-Adapter/tree/main should be saved in stable-diffusion-webui\models\ControlNet. I used for preproccesor ip-adapter_clip_sd15 and for model ip-adapter_face_sd15.

![Alt text](image.png)

# Virtual Painting Photobooth frontend setup
## Installation
Ensure a recent Python 3 is installed and photobooth.py, folders "static" and "templates" are saved in a convenient location on disk. Install any required dependencies using:

pip install -r requirements.txt

# File Structure
photobooth.py: Main Flask application script.
templates/: Folder containing HTML templates (index.html, result.html).
static/: Folder containing static files such as the background image.
models/: Directory for storing the Stable Diffusion model files (if applicable).
Customization

## Settings
For now, all configuration options are just hardcoded at the top of the script; open it in any self-respecting (or at least whitespace-respecting) text editor, and adjust the items listed under *User Configurable Settings* as desired. There are several potentially mission-critical settings here, including the ip/port of the WebUI backend (if separate from the frontend or non-default port).

# Styling: Modify style.css to change the application's appearance.
Painter Styles: Edit photobooth.py to add or modify the painter styles.

# Troubleshooting
Webcam Access: Ensure your browser has permission to access the webcam.
Stable Diffusion API: Verify that the Stable Diffusion API is running and accessible.
