import pandas as pd
import numpy as np
from nlptoolsjp.file_system import *
from gensim.models import word2vec
from nlptoolsjp.norm import *
from nlptoolsjp.morpheme import *
from sklearn.feature_extraction.text import TfidfVectorizer


# file_list  = glob("tablog_userdata/*.json")
# test_list = [file_load(file) for file in glob("tablog_usr/user*.json")]
# data_list = sum([file_load(file) for file in glob("tablog_userdata/*.json")],[])
# for d,data in enumerate(test_list):
#     for da in data:
#         if len(da["url"]) > 60:
#             print(file_list[d])
#             exit(1)
# data_list = [{"url":data["shop_url"],"店名":data["店名"]} for data in data_list]
# data_df = pd.DataFrame(data_list)
# data_df.drop_duplicates(subset=['店名'],inplace=True)
# file_create(data_df,"shop2.csv")

class Shop:
    def __init__(self,wd2vc_file_path=None,shop_file_path=None):
        self.wd2vc_model = word2vec.Word2Vec.load(wd2vc_file_path)
        self.shop_data = file_load(shop_file_path)
        self.genre_dict = file_load("genre_data.json")
        self.name = self.shop_data["店名"]
        self.comment = self.shop_data["口コミ"]
        self.url = self.shop_data["url"]
        self.genre = self.shop_data["ジャンル"]
        self.select_word = self.shop_data["word"]
        self.review = self.shop_data["評価"]
        self.place = self.shop_data["住所"]
        self.genre_id = self.genre_id[self.shop_data["ジャンル"]]
        self.select_word_vector = {k:0 for k in self.select_word}
        self.shop_vector = None

    def word_select(self):
        speech_list = ["名詞","形容詞","形容動詞"]
        ban_detail = ["非自立","接尾"]
        comment_data = clean_text(data)
        comment_data = [comment_data[i].split("。") for i in range(len(comment_data))]
        comment_data = [remove_str(_data) for _data in comment_data]
        for c,sub_com in enumerate(comment_data):
            dataset = []
            kind_dict = {}
            detail_kind_dict = {}
            # print(sub_com)
            for j,com in enumerate(sub_com):
                kind, sentence = morpheme(re.sub(r"l*","",com),kind=True,nelogd=True)
                sub = [kind[se]["endform"] if kind[se]["endform"]!="*" else se for se in sentence]
                k_dic = {kind[se]["endform"]:kind[se]["speech"] for se in sentence}
                detailk_dic = {kind[se]["endform"]:kind[se]["detail_speech"][0] for se in sentence}
                dataset.append(' '.join(sub))
                kind_dict.update(k_dic)
                detail_kind_dict.update(detailk_dic)
                # comment_data = [' '.join(morpheme(remove_str(com),nelogd=True)) for com in comment_data]
            vectorizer = TfidfVectorizer(smooth_idf = False)
            values = vectorizer.fit_transform(dataset).toarray()
                # words = vectorizer.get_feature_names()
            word_dict = {"doc_num":[],"word":[],"kind":[],"detail_kind":[],"vector":[]}
            for i in range(len(dataset)):
                for w,vec in zip(dataset[i].split(' '),values[i]):
                    try:
                        if vec > 0 and kind_dict[w] in speech_list and detail_kind_dict[w] not in ban_detail and w not in word_dict["word"]:
                            word_dict["doc_num"].append(c+1)
                            word_dict["word"].append(w)
                            word_dict["vector"].append(vec)
                            word_dict["kind"].append(kind_dict[w])
                            word_dict["detail_kind"].append(detail_kind_dict[w])
                    except:
                        continue
            if c==0:
                df = pd.DataFrame(word_dict)
            else:
                sub_df = pd.DataFrame(word_dict)
                df = pd.concat([df,sub_df])
        d = df['word'].value_counts()
        self.select_word = d.head(10)["word"].tolist()

    def word_vector_create(self):
        self.select_word_vector = {word:self.wd2vc_model.wv.get_vector(word) for word in self.select_word}

    def vector_concat(self):
        genre_vector = np.full((1,200),self.genre_id)
        review_vector = np.full((1,200),self.review)
        word_vector = np.array([vec for vec in self.select_word_vector.values()])
        self.shop_vector = np.concatenate([genre_vector,review_vector,word_vector])
    
        
    

