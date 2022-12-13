import torch
from torch.nn import Embedding
from nlptoolsjp.file_system import *
from nlptoolsjp.norm import clean_text
from torch_geometric.data import Data


class ShopGraphDataset():
    def __init__(self,user_data,shop_data_list,date,vector_size=200):
        self.user_name = user_data["user"].drop_duplicates().tolist()
        self.user_data = user_data
        self.date = date
        embeding = Embedding(len(self.user_name),vector_size)
        self.shop_name = [clean_text(shop["名前"],norm_op=False) for shop in shop_data_list] 
        user_x = embeding
        shop_x = torch.tensor([torch.from_numpy(shop["shop_vector"])  for shop in shop_data_list])
        self.x = torch.cat([user_x,shop_x])
        self.edge_index = None
    
    def index_edge_create(self):
        edge_list = []
        for user in self.user_name:
            user_df = self.user_data[user]
            user_shop = user_df["店名"].tolist()
            user_review = user_df[self.date].tolist()
            edge = [0 for i in range(len(self.user_name))]
            edge += [review if user_shop==shop else 0 for user_shop,shop,review in zip(user_shop,self.shop_name,user_review)]
            edge_list.append(edge)
        edge_list += [0 for i in range(len(self.user_name)+len(self.shop_name))]
        self.edge_index = torch.tensor(edge_list)
    
    def load_dataset(self):
        self.index_edge_create()
        return Data(x=self.x,edge_index = self.edge_index)


if __name__=="__main__":
    shop_data = ""
    user_data = file_load("csv_data\user\user_lunch_data.csv")
    data = ShopGraphDataset(user_data="")
    dataset = data.load_dataset()

