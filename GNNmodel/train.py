from dataset import ShopGraphDataset
from gnn import VariationalGCNEncoder
from torch_geometric.nn import VGAE
import torch
from torch_geometric.utils import train_test_split_edges
from torch.optim import AdamW
from nlptoolsjp.file_system import *
import time
from datetime import datetime
from gensim.models import word2vec
import sys
sys.path.append("..")
from shop import Shop


print(datetime.now())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
user_lunch_data = file_load("../csv_data/user/user_lunch_data.csv")
user_dinner_data = file_load("../csv_data/user/user_dinner_data.csv")
wd2vec_model= word2vec.Word2Vec.load("../word2vec\word2vec_model/food_Skip-gram100-5.model")
shop_data = file_load("../shop_data_v4.json")
shop_data_list = [Shop(shop_data=shop,wd2vc_model=wd2vec_model) for name,shop in shop_data.items()]
epoch = 50
dataset_module = ShopGraphDataset(user_data = user_dinner_data,shop_data_list = shop_data_list,date="夜",vector_size=1200)
dataset = dataset_module.load_dataset()
print(dataset)
split_dataset = train_test_split_edges(dataset)
edge_feature = dataset.x.to(device)
train_data_edge_index = split_dataset.train_pos_edge_index.long().to(device)
train_data_edge_attr = split_dataset.train_pos_edge_attr.double().to(device)
test_pos_edge_index = split_dataset.test_pos_edge_index.long().to(device)
test_neg_edge_index = split_dataset.test_neg_edge_index.long().to(device)
test_pos_edge_attr = split_dataset.test_pos_edge_attr.double().to(device)
input_size = 1200
output_size = 32
model2 = VGAE(VariationalGCNEncoder(input_size=input_size,output_size=output_size))
model = model2.double().to(device)
optimizer = AdamW(model.parameters(), lr=0.001)
for e in range(1,epoch+1):
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
torch.save(model,'model/dinner_vgae_v2.pth')