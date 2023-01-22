from app.system.shop import Shop
from glob import glob
from nlptoolsjp.file_system import *


data = {}
cloased_data = file_load("csv_data/closed_shop.csv")
word2vec_path = "word2vec/word2vec_model/food_Skip-gram100-5.model"
for f,file in enumerate(glob("tablog_data/*.json")):
    if file_load(file)["口コミ"] == []:
        continue
    shop = Shop(shop_file_path=file,wd2vc_file_path=word2vec_path)
    if shop.shop_data["url"] in cloased_data["url"].tolist():
        continue
    try:
        data[shop.shop_data["店名"]] = shop.save_json(file_op=False)  
    except:
        print(file)
        exit(1) 
    # try:
    #     shop.word_vector_create(wd2vc_file_path=word2vec_path)
    #     shop.id_select()
    #     shop.vector_concat()
    # except:
    #     print(file)
    #     continue
    # data[shop.shop_data["店名"]] = shop.shop_data
file_create(data,"../data/shop_json/shop_data_v4.json")