from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import cv2
from keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = ""
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route("/")
def mainIndex():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = 1
        # user = db_session.query(User).filter_by(username=username).first()
        if user != username:
            return render_template('index.html')
        user = User(username, password)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = 1
        # user = User.query.filter_by(username=username, password=password).first()
        if user != username:
            # Login successful
            return render_template('index.html')
        else:
            # Login failed
            return render_template('index.html')
    return render_template('login.html')

NAME = ""
PATH = ""
i = 0
j = 0



@app.route('/prediction1', methods=['POST'])
def predictor1():
    global i
    if i == 0:
        global model1
        model1 = load_model("static/models/model_1.h5")
    image = request.files['image']
    name = request.form.get('name')
    global NAME
    NAME = name
    print(f"Name = {name}")
    path = fr'static/user_images/{name}.jpg'
    global PATH
    PATH = path
    image.save(path)
    image = Image.open(image.stream)
    image = image.resize((224, 224))
    image.save(path)
    image = image.convert('RGB')
    image = cv2.imread(path)
    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)
    result = model1.predict(img)
    result = result.squeeze()
    if result > 0.5:
        print("Tumor")
        p = result.squeeze() * 100
        return render_template('prediction1.html', data=[f"TUMOR DETECTED", name])
    else:
        p = 100 - (result.squeeze() * 100)
        print("No tumor")
        return render_template('prediction1.html', data=[f"NO TUMOR DETECTED", name])

@app.route('/prediction2', methods=['POST'])
def predictor2():
    global j
    if j == 0:
        global model2
        model2 = load_model("static/models/model_2.h5")
    # model2 = load_model("static\models\model_2.h5")
    image = request.files['image']
    name = request.form.get('name')
    global NAME
    NAME = name
    print(f"Name = {name}")
    path = fr'static/user_images/{name}.jpg'
    global PATH
    PATH = path
    image.save(path)
    image = Image.open(image.stream)
    image = image.resize((224, 224))
    image.save(path)
    image = image.convert('RGB')
    image = cv2.imread(path)
    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)
    result = model2.predict(img)
    result = result.squeeze()
    if result > 0.5:
        print("Tumor")
        p = result.squeeze() * 100
        return render_template('prediction2.html', data=[f"Tumor detected", name])
    else:
        p = 100 - (result.squeeze() * 100)
        print("No tumor")
        return render_template('prediction2.html', data=[f"No Tumor detected", name])


@app.route('/load_img')
def load_img():
    # return render_template('index.html', data=PATH)
    global PATH, NAME
    print(PATH, NAME)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{NAME}.jpg')
    print(full_filename)
    render_template('prediction1.html', name=NAME)
    # return redirect(url_for('static', path=PATH), code=301)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
    app.config['UPLOAD_FOLDER'] = PATH
    # app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
