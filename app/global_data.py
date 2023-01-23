from system.shop import Shop
from nlptoolsjp.file_system import *
from gensim.models import word2vec

DICT_DATA = file_load("data/shop_data_v4.json")
wd2vec_path = "data/model/word2vec/tablog_Skip-gram100-5.model"
wd2vec_model= word2vec.Word2Vec.load(wd2vec_path)
SHOP_DATA = [Shop(shop_data=shop,wd2vc_model=wd2vec_model) for name,shop in DICT_DATA.items()]