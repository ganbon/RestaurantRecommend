import gensim
from nlptoolsjp.file_system import *
from nlptoolsjp.morpheme import morpheme
import pandas as pd



food_model = gensim.models.Word2Vec.load("..\word2vec_model/food_Skip-gram100-5.model")
# print(food_model.wv["ハチミツ"])
all_word = food_model.wv.index_to_key
data_list = []
kind_list = ["名詞","形容詞","形容動詞"]
for word in all_word:
    speech,_ = morpheme(word,kind=True,neologd=True)
    if speech[_[0]]['speech'] not in kind_list:
        continue  
    target_list = [word]
    w_list = food_model.wv.most_similar(word,topn=50)
    for w in w_list:
        s,_= morpheme(w[0],kind=True,neologd=True)
        if s[_[0]]["speech"] in kind_list:
            target_list.append(w)
        if len(target_list) == 11:
            break
    if len(target_list) == 11:
        data_list.append(target_list)
    else:
        print(target_list)
food_df = pd.DataFrame(data_list,columns=["target","near1","near2","near3","near4","near5","near6","near7","near8","near9","near10"])
file_create(food_df,"csv_data/food_word5.csv")