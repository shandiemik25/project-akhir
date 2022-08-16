"""
Application that predicts heart disease percentage in the population of a town
based on the number of bikers and smokers. 

Trained on the data set of percentage of people biking 
to work each day, the percentage of people smoking, and the percentage of 
people with heart disease in an imaginary sample of 500 towns.

"""

import pandas as pd
import numpy as np
from flask import Flask, request, render_template
import pickle
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

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
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
        elif n == 50:
            return "Uang Lima Puluh Ribu Rupiah"
        else :
            return "Uang Seratus Ribu Rupiah"

    ref_new = db.reference('Output')
    nom_ref_new = ref_new.child('Output_nominal')

    def testing(r, g, b):

        features = pd.DataFrame([[r,g,b]], columns=['R', 'G', 'B'])
        prediction = model.predict(features)

        #int_features = [float(x) for x in request.form.values()] #Convert string inputs to float.
        #features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
        #prediction = model.predict(features)  # features Must be in the form [[a, b]]

        output = str(output_lable(prediction[0]))
        ref_new.update({
            'Output_nominal': output
        })
        print(output)

    testing(ref_r.get(), ref_g.get(), ref_b.get())
    return render_template('index.html')

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output
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
        elif n == 50:
            return "Uang Lima Puluh Ribu Rupiah"
        else :
            return "Uang Seratus Ribu Rupiah"

    ref_new = db.reference('Output')
    nom_ref_new = ref_new.child('Output_nominal')

    def testing(r, g, b):

        features = pd.DataFrame([[r,g,b]], columns=['R', 'G', 'B'])
        prediction = model.predict(features)

        #int_features = [float(x) for x in request.form.values()] #Convert string inputs to float.
        #features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
        #prediction = model.predict(features)  # features Must be in the form [[a, b]]

        output = str(output_lable(prediction[0]))
        ref_new.update({
            'Output_nominal': output
        })
        print(output)

    testing(ref_r.get(), ref_g.get(), ref_b.get())


#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).

if __name__ == "__main__":
    app.run()