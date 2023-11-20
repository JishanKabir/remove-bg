from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

def remove_background(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_not(thresh)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result

@app.route('/removebg', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found'})

    image_file = request.files['image']
    nparr = np.fromstring(image_file.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Remove background
    removed_bg = remove_background(img_np)

    # Encode image to base64
    _, img_encoded = cv2.imencode('.png', removed_bg)
    img_bytes = img_encoded.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return jsonify({'result_image': img_base64})

if __name__ == '__main__':
    app.run(debug=True)
