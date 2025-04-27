from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from tensorflow.keras.applications.vgg16 import preprocess_input

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your trained model
model = load_model("VGG16_DR.keras")  # Update path if needed
target_size = (224, 224)  # Update to match your model input size

# Define class labels and optional descriptions
labels = {
    0: ("Mild", 
        "Mild Nonproliferative Diabetic Retinopathy (NPDR): "
        "Early signs of DR are present, such as microaneurysms — small bulges in the blood vessels of the retina that may leak fluid. "
        "Vision is typically unaffected at this stage, but routine monitoring is advised."),

    1: ("Moderate", 
        "Moderate Nonproliferative Diabetic Retinopathy: "
        "As the disease progresses, blood vessels that nourish the retina may swell and distort. "
        "There may be some blood and fluid leakage, and symptoms like blurred vision may begin to appear."),

    2: ("No DR", 
        "No Diabetic Retinopathy: "
        "The retina appears healthy with no visible signs of damage or leakage. "
        "Regular check-ups are still important, especially for individuals with diabetes."),

    3: ("Proliferative DR", 
        "Proliferative Diabetic Retinopathy (PDR): "
        "The most advanced and vision-threatening stage of DR. "
        "Abnormal new blood vessels grow on the retina, which can rupture and bleed into the eye. "
        "This stage can lead to permanent vision loss without treatment."),

    4: ("Severe", 
        "Severe Nonproliferative Diabetic Retinopathy: "
        "A significant number of retinal blood vessels are blocked, depriving areas of the retina of blood supply. "
        "This stage is a precursor to proliferative DR, and urgent treatment is usually needed to prevent further progression.")
}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Preprocessing for VGG16
        img = load_img(filepath, target_size=target_size)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # Use this if you used VGG16 during training

        # Predict
        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction))
        label, description = labels[predicted_class]

        return jsonify({
            "image_url": f"/{filepath}",
            "prediction": label,
            "description": description
        })


    return jsonify({"error": "Something went wrong"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

