from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from title_detection import load_model, load_image, RunInference

app = Flask(__name__)

def Run_Image_Processing(image, title):
    # TODO: Run title detection
    image_path = "InputImage.jpg.jpg"
    img = load_image(image_path, 0.4)

    output_image, title_list = RunInference(img, net, output_layers, confidence_threshold=0.3, nms_threshold=0.5, save_image=False)


    return title_list

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'No image selected'}), 400
    
    # Parse additional fields from the request
    title = request.form.get('title', '').strip()

    # Basic validation for title
    if len(title) == 0:
        return jsonify({'message': 'Title cannot be empty'}), 400

    if len(title) > 100:
        return jsonify({'message': 'Title exceeds maximum length of 100 characters'}), 400
    # print(title)

    # Save image
    file.save('InputImage.jpg')

    # Convert file to PIL Image object
    try:
        image = Image.open(file)
    except Exception as e:
        return jsonify({'message': f'Error opening image file: {str(e)}'}), 400


    # TODO: Process the image file here
    result = Run_Image_Processing(image, title)
    status = "Found" if result else "Not Found"

    return jsonify({'message': f'The book {title} is {status}'}), 200

@app.route('/')
def hello_world():
    return 'This is my first API call!'

weights_path = "yolov3_custom_last.weights"
config_path = "yolov3_custom.cfg"
net, output_layers = load_model(weights_path, config_path)

if __name__ == '__main__':
    
    app.run()