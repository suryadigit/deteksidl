from flask import Flask, request, jsonify
from flask_cors import CORS  # Import flask_cors untuk menangani CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Menambahkan CORS ke aplikasi Flask
CORS(app, origins=["http://localhost:5173"])  # Mengizinkan akses dari localhost:5173

# Load model
MODEL_PATH = "lstm_image_classifier.h5"
model = load_model(MODEL_PATH)

# Fungsi untuk memproses gambar
def preprocess_image(image, target_size=(48, 48)):
    image = image.convert("L")  # Konversi gambar ke grayscale
    image = image.resize(target_size)  # Resize gambar sesuai target_size
    image_array = np.array(image) / 255.0  # Normalisasi piksel gambar
    image_array = image_array.reshape(1, target_size[0], target_size[1])  # Sesuaikan bentuk gambar untuk model
    return image_array

# Endpoint untuk menerima unggahan file dan melakukan prediksi
@app.route("/upload", methods=["POST"])
def predict():
    label = ["marah", "jijik", "takut", "senang", "datar", "sedih", "terkejut"]
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Membuka gambar dari file yang diunggah
        image = Image.open(file)
        # Memproses gambar untuk prediksi
        processed_image = preprocess_image(image)
        # Melakukan prediksi menggunakan model
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)
        confidence = float(np.max(prediction))
        # Mengembalikan hasil prediksi dalam format JSON
        return jsonify({
            "predicted_class": label[int(predicted_class)],
            "confidence": confidence
        })
    except Exception as e:
        # Jika ada kesalahan dalam pemrosesan, kembalikan error
        return jsonify({"error": str(e)}), 500

# Entry point untuk menjalankan aplikasi Flask
if __name__ == "__main__":
    # Menjalankan Flask di host 0.0.0.0 agar dapat diakses dari luar
    app.run(host="0.0.0.0", port=5000)
