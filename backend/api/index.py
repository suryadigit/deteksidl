from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load model
MODEL_PATH = "lstm_image_classifier.h5"
model = load_model(MODEL_PATH)

def preprocess_image(image, target_size=(48, 48)):
    image = image.convert("L")  # Konversi ke grayscale
    image = image.resize(target_size)  # Resize ke ukuran target
    image_array = np.array(image) / 255.0  # Normalisasi piksel
    image_array = image_array.reshape(1, target_size[0], target_size[1])  # Sesuaikan bentuk untuk model
    return image_array

@app.route("/upload", methods=["POST"])
def predict():
    label = ["marah", "jijik", "takut", "senang", "datar", "sedih", "terkejut"]
    
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

# Entry point untuk Vercel
if __name__ == "__main__":
    app.run()
