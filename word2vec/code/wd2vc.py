from gensim.models import word2vec
from glob import glob
from nlptoolsjp.morpheme import morpheme
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import *


file_list = glob("hotpepper/*.json")
kind_list = ["形容詞","形容動詞"]
word_list = []
for file in file_list:
    data = file_load(file)
    if data["口コミ"] != []:
        for d in data["口コミ"]:
            d = remove_str(clean_text(d))
            kind,sentence = morpheme(d,kind=True,nelogd=True)
            # word_list.append([kind[s]["endform"] for s in sentence if kind[s]["speech"] in kind_list])
            word_list.append([kind[s]["endform"] for s in sentence])
# d = {}
# for w in word_list:
#     if w in d.keys():
#         d[w] += 1
#     else:
#         d[w] = 1
# print(d)
model = word2vec.Word2Vec(sg=1,sentences=word_list,vector_size=200,min_count=2, window=5, epochs=20)
model.save("word2vec_model/food_Skip-gram4.model")
                