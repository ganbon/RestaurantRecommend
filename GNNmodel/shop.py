import pandas as pd
import numpy as np
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import *
from nlptoolsjp.morpheme import *
from sklearn.feature_extraction.text import TfidfVectorizer


class Shop:
    def __init__(self,shop_file_path=None,shop_data=None,wd2vc_model=None):
        if shop_file_path == None:
            self.shop_data = shop_data
        else:
            self.shop_data = file_load(shop_file_path)
        self.genre = self.shop_data["ジャンル"]
        self.review = self.shop_data["評価"]
        if "genre_id" in list(self.shop_data.keys()):
            self.genre_id = self.shop_data["genre_id"]
        self.wd2vc_model = wd2vc_model

    # テキスト正規化
    def shop_text_clean(self):
        self.shop_data["店名"] = clean_text(self.shop_data["店名"],norm_op=False)
        self.shop_data["ジャンル"] = clean_text(self.shop_data["ジャンル"],norm_op=False)
        self.shop_data["口コミ"] = clean_text(self.shop_data["口コミ"],norm_op=False)

    # 重要度の高いword選択
    def word_select(self):
        token = self.wd2vc_model.wv.index_to_key
        speech_list = ["名詞","形容詞","形容動詞"]
        ban_detail = ["非自立","接尾","数","代名詞"]
        comment_data = self.shop_data["口コミ"]
        comment_data = [comment_data[i].split("。") for i in range(len(comment_data))]
        comment_data = [remove_str(_data) for _data in comment_data]
        for c,sub_com in enumerate(comment_data):
            dataset = []
            kind_dict = {}
            detail_kind_dict = {}
            for j,com in enumerate(sub_com):
                if com=="":
                    continue
                kind, sentence = morpheme(re.sub(r"l+","",com),kind=True,nelogd=True)
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
                    if w in token:
                        try:
                            if vec > 0 and w in kind_dict.keys() and kind_dict[w] in speech_list and \
                                detail_kind_dict[w] not in ban_detail and w not in word_dict["word"]: 
                                word_dict["doc_num"].append(c+1)
                                word_dict["word"].append(w)
                                word_dict["vector"].append(vec)
                                word_dict["kind"].append(kind_dict[w])
                                word_dict["detail_kind"].append(detail_kind_dict[w])  
                        except:
                            print(sub_com)  
                    else:
                        continue
            if c==0:
                df = pd.DataFrame(word_dict,index=word_dict["word"])
            else:
                sub_df = pd.DataFrame(word_dict,index=word_dict["word"])
                df = pd.concat([df,sub_df])
        comment_word = df['word'].value_counts().head(10).index.to_list()
        self.shop_data["word"] = {w:df.loc[w].values.tolist()[-1] for w in comment_word}
        return comment_word

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
    def vector_concat(self,vector_size=100):
        genre_vector = np.full((1,vector_size),self.genre_id*0.1)
        review_vector = np.full((1,vector_size),self.review/5*0.5)
        word_vector = np.array([ self.wd2vc_model.wv[word] for word in self.shop_data["word"].keys()])
        shop_vector = np.concatenate([genre_vector,review_vector,word_vector])
        if len(list(self.shop_data["word"].keys())) < 10:
            shop_vector = np.concatenate([shop_vector,np.zeros((10-len(list(self.shop_data["word"].keys())),100))])
        return shop_vector

    # 保存形式
    def save_json(self,file_name=None,file_op=True):
        self.shop_text_clean()  
        self.word_select()
        self.id_select()    
        self.shop_data.pop("口コミ")
        if file_op:
            file_create(self.shop_data,file_name)
        return self.shop_data


if __name__=="__main__":
    test = Shop(shop_file_path="tablog_data\\100時間カレー ゆめタウン高松店.json")
    test.save_json("a.json")
    print(list(test.shop_data["word"].keys()))
    data = test.vector_concat()
    # test2 = Shop(shop_file_path="a.json")
    # print(torch.from_numpy(np.ravel(test2.shop_vector)))
    # print(type(np.ravel(test2.shop_vector)))
    # print(test.shop_data["店名"])
    # print(test2.comment_word_vector)