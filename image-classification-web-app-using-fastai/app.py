from fastai.vision import load_learner, open_image
from flask import Flask, render_template, request

clf = load_learner("model", "fashion-classifier.pkl")
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_prediction():
    if request.method == 'POST':
        image_file = request.files['image-file']
        image = open_image(image_file)
        pred = clf.predict(image)[0]
        return render_template('home.html', label=pred)
    else: 
        return render_template('home.html')