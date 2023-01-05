from dataset import ShopGraphDataset
import torch
import pandas as pd
from nlptoolsjp.file_system import *
import sys
sys.path.append("..")
from shop import Shop


target = file_load("test.csv")
target_shop = target["店名"].tolist()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
user_lunch_data = target[target["昼"]!=0]
shop_data = file_load("../shop_data_v2.json")
shop_data_list = [Shop(shop_data=shop) for name,shop in shop_data.items()]
dataset_module = ShopGraphDataset(user_data = user_lunch_data,shop_data_list = shop_data_list,date="昼")
shop_name = dataset_module.shop_name
user_len = len(dataset_module.user_name)
dataset = dataset_module.load_dataset()
print(dataset)
node_feature = dataset.x.to(device)
edge_index = dataset.edge_index.long().to(device)
print(edge_index)
edge_attr = dataset.edge_attr.double().to(device)
print(edge_attr)
model = torch.load('model/lunch_vgae.pth').to(device)
z = model.encode(node_feature,edge_index,edge_attr)
result = model.decoder.forward_all(z)
# print(result.size())
# print(result[target_user_index][2000:2100])
# result = torch.matmul(z,z.T)
# print(result[target_user_index])
# print(z.size())
# print(z)
# print(torch.matmul(z,z.T).size())
# print(neg_pred.size())
_,rank = torch.topk(result[0],20)
print(rank)
# print(shop_name[-1])
for i,r in enumerate(rank):
    if shop_name[r-user_len] in target_shop or r==0:
        continue
    print(shop_name[r-user_len])
    print(result[0][r])
    print(shop_data[shop_name[r-user_len]]["url"])