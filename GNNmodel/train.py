from dataset import ShopGraphDataset
from gnn import UserVectorGNN,VariationalGCNEncoder
from torch_geometric.nn import VGAE
import torch
import numpy as np
from torch.nn import L1Loss
from torch_geometric.utils import train_test_split_edges
from torch.optim import AdamW
from nlptoolsjp.file_system import *
from tqdm import tqdm
import time
import sys
sys.path.append("..")
from shop import Shop

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
user_lunch_data = file_load("../csv_data/user/user_lunch_data.csv")
user_dinner_data = file_load("../csv_data/user/user_dinner_data.csv")
shop_data = file_load("../shop_data.json")
shop_data_list = [Shop(shop_data=shop) for shop in shop_data]
for i,s in enumerate(shop_data_list):
    if len(np.ravel(s.shop_vector)) != 2400:
        shop_data_list[i].shop_vector = np.concatenate([s.shop_vector,np.zeros((10-len(s.comment_word),200))])
epoch = 20
dataset_module = ShopGraphDataset(user_data = user_lunch_data,shop_data_list = shop_data_list,date="昼")
dataset = dataset_module.load_dataset()
dataset = dataset
split_dataset = train_test_split_edges(dataset)
edge_feature = dataset.x.to(device)
train_data_edge_index = split_dataset.train_pos_edge_index.long().to(device)
train_data_edge_attr = split_dataset.train_pos_edge_attr.double().to(device)
test_pos_edge_index = split_dataset.test_pos_edge_index.long().to(device)
test_neg_edge_index = split_dataset.test_neg_edge_index.long().to(device)
test_pos_edge_attr = split_dataset.test_pos_edge_attr.double().to(device)
# print(edge_feature.dtype,train_data_edge_index.dtype,train_data_edge_attr.dtype,test_pos_edge_index.dtype,test_neg_edge_index.dtype,test_pos_edge_attr.dtype)
# exit(1)
input_size = 2400
output_size = 16
model1 = UserVectorGNN(input_size=input_size,output_size=output_size)
# model = model1
model2 = VGAE(VariationalGCNEncoder(input_size=input_size,output_size=output_size))
model = model2.double().to(device)
# loss_function = L1Loss()
optimizer = AdamW(model.parameters(), lr=0.001)
for e in tqdm(range(epoch)):
    model.train()
    optimizer.zero_grad()
    z = model.encode(edge_feature, train_data_edge_index,train_data_edge_attr)
    recon_loss = model.recon_loss(z, train_data_edge_index)
    kl_loss = (1 / dataset.num_nodes) * model.kl_loss()
    loss = recon_loss + kl_loss
    loss.backward(retain_graph=True)
    optimizer.step()
    model.eval()
    with torch.no_grad():
        z = model.encode(edge_feature,train_data_edge_index,train_data_edge_attr)
        auc,ap = model.test(z,test_pos_edge_index,test_neg_edge_index)
        print(f"epoch:{e} AUC:{auc} AP:{ap} loss:{loss}")
    time.sleep(2)
torch.save(model, 'vgae.pth')