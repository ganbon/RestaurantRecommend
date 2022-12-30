from shop import Shop
from glob import glob
from nlptoolsjp.file_system import *

data = {}
cloased_data = file_load("csv_data/closed_shop.csv")
word2vec_path = "word2vec/word2vec_model/tablog_Skip-gram5.model"
for f,file in enumerate(glob("tablog_data/*.json")):
    if file_load(file)["口コミ"] == []:
        continue
    shop = Shop(shop_file_path=file)
    if shop.comment == [] or shop.shop_data["url"] in cloased_data["url"].tolist():
        continue
    shop.shop_text_clean()   
    try:
        shop.word_vector_create(wd2vc_file_path=word2vec_path)
        shop.id_select()
        shop.vector_concat()
    except:
        print(file)
        continue
    data[shop.shop_data["店名"]] = shop.shop_data
file_create(data,"shop_data_v2.json")