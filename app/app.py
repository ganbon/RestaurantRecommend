from flask import Flask, request, make_response,jsonify,send_file
from nlptoolsjp.file_system import *
from flask_cors import CORS
from system.search import search_shop
from system.recommend import recommend
import pandas as pd
from global_data import SHOP_DATA

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/search',methods=['GET','POST'])
def search_result():
    data = request.get_json()
    keyword = data['sentence']
    result = search_shop(keyword,SHOP_DATA)
    response = [{"url":shop.shop_data["url"],
                "name":shop.shop_data["店名"],
                "genre":shop.shop_data["ジャンル"],
                "review":shop.shop_data["評価"],
                "place":shop.shop_data["住所"]} for shop in result]
    return make_response(jsonify(response))

@app.route('/visited',methods=['GET','POST'])
def bookmark():
    data = request.get_json()
    user_data = file_load("data/csv/user.csv")
    user_data = pd.concat([user_data,pd.DataFrame(data)])
    file_create(user_data,"data/csv/user.csv")

@app.route('/recommend',methods=['GET','POST'])
def recommend_result():
    user_data = file_load("data/csv/user.csv")
    lunch_data = recommend(user_data,SHOP_DATA,model_path="data/model/lunch_vgae.pth",date="昼")
    dinner_data = recommend(user_data,SHOP_DATA,model_path="data/model/dinner_vgae.pth",date="夜")
    return lunch_data,dinner_data

if __name__ == "__main__":
    app.run(debug=True)
