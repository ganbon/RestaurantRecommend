from nlptoolsjp.file_system import *
from glob import glob
from nlptoolsjp.norm import *
from datetime import datetime


file_path_list = glob("../data/tablog_userdata/*.json")
user_data_list = []
shop_data = {"url":[],"店名":[]}
for file in file_path_list:
    data_list = file_load(file)
    for data in data_list:
        if data["訪問日時"] is None:
            dtime = None
        else:
            dtime = datetime.strptime(data["訪問日時"].replace("訪問",""),"%Y/%m")
        user_status = {"user":remove_str(file.split("\\")[1],remove_str=r"\-[0-9]*\.json")
                        ,"店名":data["店名"]
                        ,"昼":data["評価"]["昼"]
                        ,"夜":data["評価"]["夜"],
                        "訪問日時":dtime}
        if data["店名"] not in shop_data["店名"]:
            shop_data["店名"].append(data["店名"])
            shop_data["url"].append(data["shop_url"])
        user_data_list.append(user_status)
df = pd.DataFrame(user_data_list)
shop_df = pd.DataFrame(shop_data)
dinner_df = df[df["夜"]!=0]
lunch_df = df[df["昼"]!=0]
file_create(df,"../data/user_data.csv")
file_create(shop_df,"../data/shop.csv")
file_create(dinner_df,"../data/user_dinner_data.csv")
file_create(lunch_df,"../data/user_lunch_data.csv")