from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

app = Flask(_name_)

# Cargar modelo preentrenado
model = ResNet50(weights='imagenet')

@app.route('/predict', methods=['POST'])
def predict():
    img_file = request.files['img']
    img_path = "./" + img_file.filename
    img_file.save(img_path)

    # Cargar imagen y procesarla
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Hacer predicción
    preds = model.predict(x)
    result = decode_predictions(preds, top=1)[0][0]
    return jsonify({
        'label': result[1],
        'confidence': float(result[2])
    })

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000)
