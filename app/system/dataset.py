import torch
from torch.nn import Embedding
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import clean_text
import numpy as np
from torch_geometric.transforms import RandomLinkSplit
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
        edge_attr = []
        src = []
        dst = []
        for u,user in enumerate(self.user_name):
            shop_list = []
            user_df = self.user_data[self.user_data["user"]==user]
            user_shop = clean_text(user_df["店名"].tolist(),norm_op=False)
            # user_review = [review - user_df[self.date].mean() for review in user_df[self.date].tolist()]
            user_review = user_df[self.date].tolist()
            for shop,review in zip(user_shop,user_review):
                if shop in shop_list:
                    continue
                try:
                    dst.append(len(self.user_name)+self.shop_name.index(shop))
                    src.append(u)
                    shop_list.append(shop)
                    edge_attr.append(review)
                except:
                    pass
        edge_list = torch.tensor([src,dst])
        self.edge_attr = torch.tensor(edge_attr)
        self.edge_index = edge_list
    
    def load_dataset(self):
        self.index_edge_create()
        return Data(x=self.x,edge_index = self.edge_index,edge_attr=self.edge_attr)


if __name__=="__main__":
    shop_data = file_load("../shop_data.json")
    shop_data_list = [Shop(shop_data=shop) for shop in shop_data]
    for i,s in enumerate(shop_data_list):
        if len(np.ravel(s.shop_vector)) != 2400:
            shop_data_list[i].shop_vector = np.concatenate([s.shop_vector,np.zeros((10-len(s.comment_word),200))])
    user_data = file_load("../csv_data/user/user_lunch_data.csv")
    data = ShopGraphDataset(user_data=user_data,shop_data_list=shop_data_list,date="昼")
    dataset = data.load_dataset()
    torch.set_printoptions(edgeitems=4000)
    # print(negative_sampling(dataset.edge_index,num_nodes=len(dataset.x)))
    # print(len(negative_sampling(dataset.edge_index,num_nodes=len(dataset.x))[0]))
    transform = RandomLinkSplit(is_undirected=True, split_labels=True)
    train_data, val_data, test_data = transform(dataset)
    print(train_data)
    print(test_data)
    print(train_data.edge_attr.double())
    # print(test_data.pos_edge_label_index)
    # print(test_data.neg_edge_label_index)
    # print(len(data.edge_index[0]))
    # print(len(data.user_name),len(data.shop_name))
    # print(dataset)
    # split_data = train_test_split_edges(dataset)
    # print(split_data)
    # print(split_data.test_neg_edge_index[:30])
    # print(split_data.test_pos_edge_index[:30])
    # print(split_data.test_neg_edge_index.size())
    # print(split_data.test_pos_edge_index.size())
    # print(dataset.num_node_features)
    # print(dataset.contains_isolated_nodes())
    # print(dataset["x"].size())
    # print(dataset["edge_index"].size())
    # torch.set_printoptions(edgeitems=4000)
    # for x in dataset["edge_index"]:
    #     print(x)