from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import os
import numpy as np
from flask_cors import CORS
import collections
collections.Iterable = collections.abc.Iterable
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
app = Flask(__name__)
CORS(app)
loadedModel = tf.keras.models.load_model("./RailTrackFaultDetection.h5")
class_name={0:'Defective', 1:'Non defective'}
def loadImg(imgPath): 
    img = tf.keras.preprocessing.image.load_img(imgPath, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route('/', methods=['POST'])
def home(): 
    if request.method == 'POST':  
        print("Received a POST request")
        file = request.files['file']
        file_path = os.path.join("./", file.filename)
        file.save(file_path)
        
        img = loadImg(file_path)
        predictions = loadedModel.predict(img)
        predicted_class = np.argmax(predictions, axis=1)
        os.remove(file_path) 
        print("Predicted class: ", class_name[predicted_class[0]])
        return jsonify({"message": "Prediction successful", "predicted_class": class_name[predicted_class[0]]})

if __name__ == '__main__':
    app.run(debug=True)
