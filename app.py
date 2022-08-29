import pandas as pd
from flask import Flask, render_template
import pickle
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("esp32andfirebase-f0541-firebase-adminsdk-5x1rd-3dcc708696.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp32andfirebase-f0541-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

ref = db.reference('/Sensor')
ref_r = db.reference('/Sensor/r')
ref_g = db.reference('/Sensor/g')
ref_b = db.reference('/Sensor/b')

#Create an app object using the Flask class. 
app = Flask(__name__)

#Load the trained model. (Pickle file)
model = pickle.load(open('models/model.pkl', 'rb'))

@app.route('/')
def home():
    def output_lable(n):
        if n == 1:
            return "Uang Seribu Rupiah"
        elif n == 2:
            return "Uang Dua Ribu Rupiah"
        elif n == 5:
            return "Uang Lima Ribu Rupiah"
        elif n == 10:
            return "Uang Sepuluh Ribu Rupiah"
        elif n == 20:
            return "Uang Dua Puluh Ribu Rupiah"
        elif n == 50:
            return "Uang Lima Puluh Ribu Rupiah"
        elif n ==100:
            return "Uang Seratus Ribu Rupiah"
        else:
            return "Uang Tidak Terdeteksi"

    ref_new = db.reference('Output')
    nom_ref_new = ref_new.child('Output_nominal')

    def testing(r, g, b):

        features = pd.DataFrame([[r,g,b]], columns=['R', 'G', 'B'])
        prediction = model.predict(features)

        output = str(output_lable(prediction[0]))
        ref_new.update({
            'Output_nominal': output
        })
        print(output)

    testing(ref_r.get(), ref_g.get(), ref_b.get())
    return """
    <meta http-equiv="refresh" content="1" /> 
    <br>The current time is {}.""".format(datetime.strftime(datetime.now(), "%d %B %Y %X"))

@app.route('/predict',methods=['POST'])
def predict():
    def output_lable(n):
        if n == 1:
            return "Uang Seribu Rupiah"
        elif n == 2:
            return "Uang Dua Ribu Rupiah"
        elif n == 5:
            return "Uang Lima Ribu Rupiah"
        elif n == 10:
            return "Uang Sepuluh Ribu Rupiah"
        elif n == 20:
            return "Uang Dua Puluh Ribu Rupiah"
        elif n == 50:
            return "Uang Lima Puluh Ribu Rupiah"
        elif n == 1000 :
            return "Uang Seratus Ribu Rupiah"

    ref_new = db.reference('Output')
    nom_ref_new = ref_new.child('Output_nominal')

    def testing(r, g, b):

        features = pd.DataFrame([[r,g,b]], columns=['R', 'G', 'B'])
        prediction = model.predict(features)

        output = str(output_lable(prediction[0]))
        ref_new.update({
            'Output_nominal': output
        })
        print(output)

    testing(ref_r.get(), ref_g.get(), ref_b.get())

if __name__ == "__main__":
    app.run()