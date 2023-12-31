from flask import Flask, render_template, jsonify, request
import os
import base64
import time

app = Flask(__name__)

# Create a folder to store uploaded images if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html', images=[])

@app.route('/pagelets')
def get_pagelets():
    images = os.listdir(UPLOAD_FOLDER)
    pagelets = []
    for i, image_name in enumerate(images):
        with open(os.path.join(UPLOAD_FOLDER, image_name), 'rb') as file:
            file_content = file.read()
            file_content = base64.b64encode(file_content).decode('utf-8')
            image_data = {
                'file': file_content,
                'description': image_name
            }
            pagelets.append(image_data)
            # Introduce a delay before sending each image
            time.sleep(1)  # Change the delay time here as needed
    return jsonify(pagelets)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({'message': 'File uploaded successfully'})
    return jsonify({'message': 'No file uploaded'})

if __name__ == '__main__':
    app.run(debug=True)
