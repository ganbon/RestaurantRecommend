from gensim.models import word2vec
import numpy as np
from nlptoolsjp.file_system import *
from sklearn.metrics.pairwise import cosine_similarity
import time


# 検索機能
def search_shop(keyword,shop_data_list):
    model = word2vec.Word2Vec.load("data/model/word2vec/tablog_Skip-gram100-5.model")
    start = time.time()
    keyword = keyword.replace("　"," ")
    keyword_list = keyword.split(" ")
    w_list = keyword_list
    v_list = [np.sum([model.wv[w] for w in w_list],axis=0)]
    # v_list = [model.wv[w] for w in w_list]
    # for s in shop_data_list:
    #     if max_kind < len(set(list(s.shop_data["word"].keys())+s.shop_data["ジャンル"]) & set(w_list)):
    #         target_shop = s
    #         target_vector = s.vector_concat()
    #         max_kind = len(set(list(s.shop_data["word"].keys())+s.shop_data["ジャンル"]) & set(w_list))
        # if len(set(list(s.shop_data["word"].keys())+s.shop_data["ジャンル"]) & set(keyword_list)) != 0:
        #     select_data.append((10,s))
    # if max_kind >= 3:
    #     for s in shop_data_list:
    #         shop_vector = s.vector_concat()
    #         select_data = [
    #         (cosine_similarity([np.ravel(target_vector[:2]),np.ravel(shop_vector[:2])])[0][0] * 0.5+mixed_similar(shop_vector[2:],target_vector[2:]),s)
    #         for s in shop_data_list
    #         ]
    # else:
    select_data = [
    (mixed_similar(list(s.shop_data["word"].keys()),keyword_list,np.array([model.wv[word] for word in s.shop_data["word"].keys()]),v_list),s)
    for s in shop_data_list
    ]
    # print(target_shop.shop_data["word"].keys())
    print(time.time()-start)
    rate_data = np.argsort(-np.array([rate[0] for rate in select_data]))
    print([select_data[index][0] for index in rate_data[:100]])
    return [select_data[index][1] for index in rate_data[:100]]

def mixed_similar(word_list,keyword_list,array1,array2):
    result = np.sum(cosine_similarity(array1,array2))/10
    if set(keyword_list)&set(word_list)==set(keyword_list):
        result += 1
    elif set(keyword_list)&set(word_list)==set(keyword_list[0]):
        result += 0.5
    elif set(keyword_list)&set(word_list)==set(keyword_list[0]):
        result += 0.25
    return result
    # rate = 0
    # for arr in array1:
    #     rate += max(cosine_similarity([arr],array2)[0])
    # return rate/len(array1)
    