import pandas as pd
import numpy as np
from nlptoolsjp.file_system import *
from gensim.models import word2vec
from nlptoolsjp.norm import *
from nlptoolsjp.morpheme import *
from sklearn.feature_extraction.text import TfidfVectorizer


class Shop:
    def __init__(self,shop_file_path=None,shop_data=None):
        if shop_file_path == None:
            self.shop_data = shop_data
        else:
            self.shop_data = file_load(shop_file_path)
        self.genre = self.shop_data["ジャンル"]
        self.review = self.shop_data["評価"]
        self.comment = self.shop_data["口コミ"]
        if "word" in self.shop_data.keys():
            self.comment_word = self.shop_data["word"]
            self.comment_word_vector = {word:np.array(vector) for word,vector in self.shop_data["comment_word_vector"].items()}
        else:
            self.comment_word = None
            self.comment_word_vector = {}
        if "shop_vector" in self.shop_data.keys():
            self.shop_vector = np.array(self.shop_data["shop_vector"])
        else:
            self.shop_vector = None
        self.genre_id = None

    # テキスト正規化
    def shop_text_clean(self):
        self.shop_data["店名"] = clean_text(self.shop_data["店名"],norm_op=False)
        self.shop_data["ジャンル"] = clean_text(self.shop_data["ジャンル"],norm_op=False)
        self.shop_data["口コミ"] = clean_text(self.shop_data["口コミ"],norm_op=False)

    # 重要度の高いword選択
    def word_select(self):
        speech_list = ["名詞","形容詞","形容動詞"]
        ban_detail = ["非自立","接尾"]
        comment_data = clean_text(self.comment)
        comment_data = [comment_data[i].split("。") for i in range(len(comment_data))]
        comment_data = [remove_str(_data) for _data in comment_data]
        for c,sub_com in enumerate(comment_data):
            dataset = []
            kind_dict = {}
            detail_kind_dict = {}
            for j,com in enumerate(sub_com):
                if com=="":
                    continue
                kind, sentence = morpheme(re.sub(r"l*","",com),kind=True,nelogd=True)
                sub = [kind[se]["endform"] if kind[se]["endform"]!="*" else se for se in sentence]
                k_dic = {kind[se]["endform"]:kind[se]["speech"] for se in sentence}
                detailk_dic = {kind[se]["endform"]:kind[se]["detail_speech"][0] for se in sentence}
                dataset.append(' '.join(sub))
                kind_dict.update(k_dic)
                detail_kind_dict.update(detailk_dic)
            vectorizer = TfidfVectorizer(smooth_idf = False)
            try:
                values = vectorizer.fit_transform(dataset).toarray()
            except:
                continue
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
        d = df['word'].value_counts().head(30).index.tolist()
        self.comment_word = d
        
    # 選択した単語ベクトル化
    def word_vector_create(self,wd2vc_file_path="word2vec/word2vec_model/tablog_Skip-gram.model"):
        wd2vc_model = word2vec.Word2Vec.load(wd2vc_file_path)
        for word in self.comment_word:
            try:
                self.comment_word_vector[word] = wd2vc_model.wv.get_vector(word)
            except:
                continue
            if len(list(self.comment_word_vector.keys())) == 10:
                break
        self.shop_data["word"] = list(self.comment_word_vector.keys())
        self.shop_data["comment_word_vector"] = {k:v.tolist() for k,v in self.comment_word_vector.items()}

    # ジャンルのid決定
    def id_select(self):
        id_list,genre_list = self.id_create()
        self.genre_id = list(set(id_list))[0]
        self.shop_data["genre_id"] = self.genre_id

    # ジャンルからidを作成
    def id_create(self):
        id_list = []
        if self.genre == None:
            return [-1]
        else:
            genre_list = [self.extract_genre(genre) for genre in clean_text(self.genre,norm_op=False).split("、")]
            self.shop_data["ジャンル"] = genre_list
            for genre in genre_list:
                for main_genre,relate_genre in self.genre_rule.items():
                    if genre == main_genre or genre in relate_genre["関連"]: 
                       id_list.append(relate_genre["id"])
            return id_list,genre_list 

    # 複数ジャンルから代表的なジャンルを決定
    def extract_genre(self,genre,jugstr="百名店",genre_path="genre_rule.json"):
        self.genre_rule = file_load(genre_path)
        if jugstr in genre:
            for main_genre,relate_genre in self.genre_rule.items():
                if main_genre in genre:
                    return main_genre
                else:
                    for relate in relate_genre["関連"]:
                        if relate in genre:
                            return relate
        else:
            return genre

    # 店ベクトル作成
    def vector_concat(self):
        genre_vector = np.full((1,200),self.genre_id*0.1)
        review_vector = np.full((1,200),self.review/5*0.1)
        word_vector = np.array([vec for vec in self.comment_word_vector.values()])
        self.shop_vector = np.concatenate([genre_vector,review_vector,word_vector])
        if len(self.shop_vector) != 2400:
            self.shop_vector = np.concatenate([self.shop_vector,np.zeros((10-len(self.comment_word),200))])
        self.shop_data["shop_vector"] = self.shop_vector.tolist()

    # とりあえず置いてる
    def save_json(self,file_name,select_op=True,genre_op=True,vector=True):
        self.shop_text_clean()  
        if select_op:
            self.word_select()
            if self.comment_word == []:
                return 
            self.word_vector_create()
        if genre_op:
            self.id_select()
        if vector:
            self.word_vector_create()
            self.vector_concat()        
        file_create(self.shop_data,file_name)




if __name__=="__main__":
    import torch
    test = Shop(shop_file_path="tablog_data/'99 BABY's CAFE.json")
    test.word_select()
    print(test.comment_word)
    # test.word_vector_create()
    # test.id_select()
    # test.vector_concat()
    # print(test.shop_data["shop_vector"])
    # print(type(test.shop_data["comment_word_vector"]["精算"]))
    # print(test.shop_data["comment_word_vector"]["精算"])
    # file_create(test.shop_data["comment_word_vector"],"a.json")
    # print(type(test.shop_data))
    test.save_json("a.json")
    test2 = Shop(shop_file_path="a.json")
    print(torch.from_numpy(np.ravel(test2.shop_vector)))
    print(type(np.ravel(test2.shop_vector)))
    # print(test2.comment_word_vector)