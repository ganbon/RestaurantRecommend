from gensim.models import word2vec
import numpy as np
from nlptoolsjp.file_system import *
from sklearn.metrics.pairwise import cosine_similarity


# 検索機能
def search_shop(keyword,shop_data_list):
    model = word2vec.Word2Vec.load("word2vec/word2vec_model/tablog_Skip-gram.model")
    select_data = []
    max_kind = 0
    target_shop = None
    w_list = [w[0] for w in model.wv.most_similar(keyword,topn=9)] + [keyword]
    for s in shop_data_list:
        if set(s.shop_data["word"]+s.shop_data["ジャンル"]) & set(w_list) != set():
            if max_kind < len(set(s.shop_data["word"]+s.shop_data["ジャンル"]) & set(w_list)):
                target_shop = s
                max_kind = len(set(s.shop_data["word"]+s.shop_data["ジャンル"]) & set(w_list))
    for s in shop_data_list:
        rate = cosine_similarity([np.ravel(target_shop.shop_vector[:2]),np.ravel(s.shop_vector[:2])])[0][0]
        rate +=  mixed_similar(target_shop.shop_vector[2:],s.shop_vector[2:])
        select_data.append((rate,s))
    select_data.sort(reverse=True)
    return [shop[1] for shop in select_data[:100]]

def mixed_similar(array1,array2):
    rate = 0
    for i in range(len(array1)):
        rate += max(cosine_similarity([array1[i]],array2)[0])
    return rate/len(array1)