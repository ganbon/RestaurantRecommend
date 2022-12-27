from flask import Flask,render_template, request
from nlptoolsjp.file_system import file_load
import os


app = Flask(__name__,static_folder='./static')


@app.route('/')
def start_site():
    if os.path.isfile("data/user/user_status.json"): 
        return render_template("index.html")
    else:
        return render_template("first_setting.html")

@app.route('/index',methods=["POST"])
def index():
    user_data = file_load("data/user/user_status.json")
    key_word = request.form.get()
    key_place = request.form.get()  
