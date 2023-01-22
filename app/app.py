from flask import Flask, request, make_response,jsonify
from nlptoolsjp.file_system import *
from flask_cors import CORS
from system.search import search_shop
from system.recommend import recommend
from datetime import datetime
import pandas as pd
from global_data import SHOP_DATA,DICT_DATA

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/search',methods=['GET','POST'])
def search_result():
    data = request.get_json()
    keyword = data['sentence']
    try:
        result = search_shop(keyword,SHOP_DATA)
    except:
        return make_response(jsonify(None))
    response = [{"url":shop.shop_data["url"],
                "name":shop.shop_data["店名"],
                "genre":' '.join(shop.shop_data["ジャンル"]),
                "review":shop.shop_data["評価"],
                "place":shop.shop_data["住所"]} for shop in result]
    return make_response(jsonify(response))

@app.route('/visited',methods=['GET','POST'])
def bookmark():
    now_date = datetime.now()
    result = {"user":"A","店名":None,"昼":0,"夜":0,"訪問日時":now_date.strftime("%Y-%m-%d")}
    data = request.get_json()
    result["店名"] = data["name"]
    result["昼"] = float(data["lunch"])
    result["夜"] = float(data["dinner"])
    user_data = file_load("data/csv/user.csv")
    if result["店名"] not in user_data["店名"]:
        result_df = pd.DataFrame(result,index=[0])
        # print(result_df)
        user_data = pd.concat([user_data,result_df])   
    else:
        user_data[user_data["店名"]==result["店名"]]["昼"] = result["昼"]
        user_data[user_data["店名"]==result["店名"]]["夜"] = result["夜"]
        user_data[user_data["店名"]==result["店名"]]["訪問日時"] = result["訪問日時"] 
    file_create(user_data,"data/csv/user.csv")
    return "ok"

@app.route('/recommend',methods=['GET','POST'])
def recommend_result():
    user_data = file_load("data/csv/user.csv")
    user_lunch_data = user_data[user_data["昼"]!=0]
    user_dinner_data = user_data[user_data["夜"]!=0]
    lunch_data = recommend(user_lunch_data,SHOP_DATA,model_path="data/model/gnn/lunch_vgae_v2.pth",date="昼")
    dinner_data = recommend(user_dinner_data,SHOP_DATA,model_path="data/model/gnn/dinner_vgae_v2.pth",date="夜")
    lunch_response = [{"url":shop.shop_data["url"],
                "name":shop.shop_data["店名"],
                "genre":' '.join(shop.shop_data["ジャンル"]),
                "review":shop.shop_data["評価"],
                "place":shop.shop_data["住所"]} for shop in lunch_data]
    dinner_resonse = [{"url":shop.shop_data["url"],
                "name":shop.shop_data["店名"],
                "genre":' '.join(shop.shop_data["ジャンル"]),
                "review":shop.shop_data["評価"],
                "place":shop.shop_data["住所"]} for shop in dinner_data]
    return make_response(jsonify({"lunch":lunch_response,"dinner":dinner_resonse}))

@app.route('/history',methods=["GET","POST"])
def bookhistory():
    user_data = file_load("data/csv/user.csv")
    history = [DICT_DATA[name] for name in user_data["店名"].tolist()]
    resonse = [{"url":shop["url"],
                "name":shop["店名"],
                "genre":' '.join(shop["ジャンル"]),
                "review":shop["評価"],
                "place":shop["住所"]} for shop in history]
    return make_response(jsonify(resonse))

@app.route('/delate',methods=["GET","POST"])
def delate():
    data = request.get_json()
    user_data = file_load("data/csv/user.csv")
    file_create(user_data[user_data["店名"]!=data["name"]],"data/csv/user.csv")
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)