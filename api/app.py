from flask import Flask, request, jsonify

app = Flask(__name__)

def Run_Image_Processing():
    # TODO: Run title detection
    print("Running and processing using AI.")
    return False

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'No image selected'}), 400
    
    # Parse additional fields from the request
    title = request.form.get('Title', '')
    print(title)

    # Save image
    file.save( title + '.jpg')

    # TODO: Process the image file here
    result = Run_Image_Processing()
    status = "Found" if result else "Not Found"

    return jsonify({'message': f'The book {title} is {status}'}), 200

@app.route('/')
def hello_world():
    return 'This is my first API call!'

if __name__ == '__main__':
    app.run()