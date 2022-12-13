from gensim.models import word2vec
from glob import glob
from nlptoolsjp.file_system import *
import re


lunchshop_data = []
dinnershop_data = []
for i in range(1,101):
    file_list = glob(f"tablog_usr/user{i}-*.json")
    data = [file_load(file) for file in file_list]
    lunch = [ re.sub(r'[\n \u3000]', '', d["店名"]) for _data in data for d in _data if d["評価"]["昼"]!=0]
    dinner = [re.sub(r'[\n \u3000]', '', d["店名"])  for _data in data for d in _data if d["評価"]["夜"]!=0]
    lunchshop_data.append(lunch)
    dinnershop_data.append(dinner)
lunch_model = word2vec.Word2Vec(sg=1,sentences=lunchshop_data,vector_size=100,min_count=2, window=5, epochs=20)
lunch_model.save("word2vec_model/lunchshop_Skip-gram.model")
dinner_model = word2vec.Word2Vec(sg=1,sentences=dinnershop_data,vector_size=100,min_count=2, window=5, epochs=20)
dinner_model.save("word2vec_model/dinnershop_Skip-gram.model")