from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from titledetection import load_model, load_image, RunInference

app = Flask(__name__)

def DetectTitlesUsingAI(imagePath):
    try:
        # Run title detection
        img = load_image(imagePath, 0.4)
        _, title_list = RunInference(img, net, output_layers, confidence_threshold=0.3, nms_threshold=0.5, save_image=False)
        return title_list
    except Exception as e:
        return f"Error processing image: {str(e)}"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'No image selected'}), 400
    
    # Save image
    file.save('InputImage.jpg')

    # Process the image file here
    title_list = DetectTitlesUsingAI('InputImage.jpg')

    if isinstance(title_list, str):
        return jsonify({'message': title_list}), 400

    return jsonify({'titles': title_list}), 200


weights_path = "yolov3_custom_last.weights"
config_path = "yolov3_custom.cfg"
net, output_layers = load_model(weights_path, config_path)

if __name__ == '__main__':
    
    app.run()