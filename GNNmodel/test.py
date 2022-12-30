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
user_lunch_data = file_load("../csv_data/user/user_lunch_data.csv")
user_dinner_data = file_load("../csv_data/user/user_dinner_data.csv")
user_lunch_data = pd.concat([user_lunch_data,target])
shop_data = file_load("../shop_data_v2.json")
shop_data_list = [Shop(shop_data=shop) for name,shop in shop_data.items()]
dataset_module = ShopGraphDataset(user_data = user_lunch_data,shop_data_list = shop_data_list,date="昼")
user_len = len(dataset_module.user_name)
target_user_index = dataset_module.user_name.index("A")
shop_name = dataset_module.shop_name
dataset = dataset_module.load_dataset()
node_feature = dataset.x.to(device)
edge_index = dataset.edge_index.long().to(device)
edge_attr = dataset.edge_attr.double().to(device)
print(dataset_module.user_name[target_user_index])
neg_dst_index = [user_len+dst for dst,shop in enumerate(shop_name) if shop_name in target_shop]
neg_src_index = [target_user_index for i in range(len(neg_dst_index))]
neg_index = torch.tensor([neg_src_index,neg_dst_index])
model = torch.load('lunch_vgae.pth').to(device)
z = model.encode(node_feature,edge_index,edge_attr)
result = model.decoder.forward_all(z)
print(result.size())
# print(result[target_user_index][2000:2100])
# result = torch.matmul(z,z.T)
# print(result[target_user_index])
# print(z.size())
# print(z)
# print(torch.matmul(z,z.T).size())
# print(neg_pred.size())
print(torch.where(result[target_user_index] > 0.9))
_,rank = torch.topk(result[target_user_index],10)
# print(rank)
for r in rank:
    print(shop_name[r-user_len])
    print(shop_data[shop_name[r-user_len]]["url"])