import numpy as np
from flask import Flask, request, jsonify, render_template
import sqlite3
import pandas as pd
import joblib


with open("models/model.sav", "rb") as model_file:
    model = joblib.load(model_file)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route('/index')
def index():
	return render_template('index.html')


@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('password','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signin.html")

        

@app.route("/notebook")
def notebook1():
    return render_template("Notebook.html")


@app.route('/predict',methods=['POST'])
def predict():
    
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    
    predict = model.predict(final4)

    if predict == 0:
        output = 'Genuine Profile Detected.'
    elif predict == 1:
        output = 'Fake Profile Detected.'

    return render_template('results.html', predicted=output)
    


if __name__ == "__main__":
    app.run(debug=True)
