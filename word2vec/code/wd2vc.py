from gensim.models import word2vec
from glob import glob
from nlptoolsjp.morpheme import morpheme
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import *


file_list = glob("../../tablog_data/*.json")
word_list = []
for f,file in enumerate(file_list):
    # print(file)
    data = file_load(file)
    if data["口コミ"] != []:
        for d in data["口コミ"]:
            text = clean_text(remove_str(d))
            kind,sentence = morpheme(text,kind=True,nelogd=True)
            # word_list.append([kind[s]["endform"] for s in sentence if kind[s]["speech"] in kind_list])
            word_list.append([kind[s]["endform"] for s in sentence if kind[s]["endform"]!="*"])
model = word2vec.Word2Vec(sg=1,sentences=word_list,vector_size=200,min_count=2, window=5, epochs=50)
model.save("../word2vec_model/food_Skip-gram5.model")
