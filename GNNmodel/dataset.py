import torch
from torch.nn import Embedding
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import clean_text
import numpy as np
from torch_geometric.utils import train_test_split_edges
from torch_geometric.data import Data
import sys
sys.path.append("..")
from shop import Shop


class ShopGraphDataset:
    def __init__(self,user_data,shop_data_list,date,vector_size=2400):
        self.user_name = list(set(user_data["user"]))
        self.user_data = user_data
        self.date = date
        embeding = Embedding(len(self.user_name),vector_size)
        self.shop_name = [shop.shop_data["店名"] for shop in shop_data_list] 
        user_x = embeding(torch.tensor([i for i in range(len(self.user_name))]))
        shop_x = torch.stack([torch.from_numpy(np.ravel(shop.shop_vector))  for shop in shop_data_list])
        self.x = torch.cat([user_x,shop_x])
        self.edge_index = None
    def index_edge_create(self):
        shop_list = []
        edge_attr = []
        src = []
        dst = []
        for u,user in enumerate(self.user_name):
            user_df = self.user_data[self.user_data["user"]==user]
            user_shop = clean_text(user_df["店名"].tolist(),norm_op=False)
            user_review = user_df[self.date].tolist()
            for shop,review in zip(user_shop,user_review):
                try:
                    dst.append(len(self.user_name)+self.shop_name.index(shop))
                    src.append(u)
                    edge_attr.append(review)
                except:
                    shop_list.append(shop)
                    pass
        edge_list = torch.tensor([src,dst])
        self.edge_attr = torch.tensor(edge_attr)
        self.edge_index = edge_list
    
    def load_dataset(self):
        self.index_edge_create()
        return Data(x=self.x,edge_index = self.edge_index,edge_attr=self.edge_attr)


if __name__=="__main__":
    shop_data = file_load("../shop_data_v2.json")
    shop_data_list = [Shop(shop_data=shop) for name,shop in shop_data.items()]
    for i,s in enumerate(shop_data_list):
        if len(np.ravel(s.shop_vector)) != 2400:
            shop_data_list[i].shop_vector = np.concatenate([s.shop_vector,np.zeros((10-len(s.comment_word),200))])
    user_data = file_load("../csv_data/user/user_lunch_data.csv")
    data = ShopGraphDataset(user_data=user_data,shop_data_list=shop_data_list,date="昼")
    dataset = data.load_dataset()
    print(dataset)
    # print(dataset.edge_index)
    split_data = train_test_split_edges(dataset)
    print(split_data)
    # print(dataset.num_node_features)
    # print(dataset.contains_isolated_nodes())
    # print(dataset["x"].size())
    # print(dataset["edge_index"].size())
    # torch.set_printoptions(edgeitems=4000)
    # for x in dataset["edge_index"]:
    #     print(x)