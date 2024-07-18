from flask import Flask, render_template, send_from_directory
from tensorflow import keras
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, send_from_directory
import os
import base64

generator_model = keras.models.load_model("models/generator_model.h5")

app = Flask(__name__)
@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        text_input = data['text_input']

        if not text_input:
            return "Text input is empty", 400

        z_dim = 100
        noise = np.random.normal(0, 1, (1, z_dim))

        words = text_input.split()
        max_words = 10
        selected_words = words[:max_words]
        encoded_text = [1 if word in selected_words else 0 for word in words]
        encoded_text += [0] * (max_words - len(selected_words))

        input_data = noise.copy()
        input_data[0, :len(encoded_text)] = encoded_text

        generated_image = generator_model.predict(input_data)[0]

        target_size = (600, 600)
        generated_image = cv2.resize(generated_image, target_size)
        
        scaled_image = (generated_image * 255).astype(np.uint8)

        img_path = "generated_image1.png"
        cv2.imwrite(img_path, scaled_image)

        retval, buffer = cv2.imencode('.png', scaled_image)
        img_bytes = buffer.tobytes()
        
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
       
        response = {
            'image': img_base64,
            'content_type': 'image/png'
        }
        return jsonify(response), 200

    except Exception as e:
        print(e)
        return "Error generating image", 500

def convert_image_to_bytes(image):
    
    retval, buffer = cv2.imencode('.png', image)
    img_bytes = buffer.tobytes()
    return img_bytes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/models")
def serve_h5_model():
    h5_file = "generator_model1.h5"

    directory = "/models/generator_model.h5"

    return send_from_directory(directory, h5_file)


@app.route("/assets/img/background/<path:filename>")
def serve_background_image(filename):
    return send_from_directory("static/img/background", filename)


if __name__ == "__main__":
    app.run(debug=True)
