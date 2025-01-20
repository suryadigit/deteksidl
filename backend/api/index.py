from flask import Flask, request, jsonify
from flask_cors import CORS 
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])  

MODEL_PATH = "lstm_image_classifier.h5"
model = load_model(MODEL_PATH)

def preprocess_image(image, target_size=(48, 48)):
    image = image.convert("L")  
    image = image.resize(target_size)  
    image_array = np.array(image) / 255.0 
    image_array = image_array.reshape(1, target_size[0], target_size[1]) 
    return image_array

@app.route("/api/upload", methods=["POST"])
def predict():
    label = ["marah", "jijik", "takut", "senang", "datar", "sedih", "terkejut"]
    print("File request diterima:", request.files)
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(file)
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)
        confidence = float(np.max(prediction))
        return jsonify({
            "predicted_class": label[int(predicted_class)],
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
