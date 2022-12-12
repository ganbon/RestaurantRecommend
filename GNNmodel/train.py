from dataset import ShopGraphDataset
from gnn import UserVectorGNN,VariationalGCNEncoder
from torch_geometric.nn import VGAE
import torch
from torch.nn import L1Loss
from torch.optim import AdamW
from nlptoolsjp.file_system import *
from tqdm import tqdm

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
user_lunch_data = file_load("../csv_data/user/user_lunch_data.csv")
user_dinner_data = file_load("../csv_data/user/user_dinner_data.csv")
shop_data = file_load("")
epoch = 20
dataset_module = ShopGraphDataset(user_lunch_data,shop_data,date="昼")
dataset = dataset_module.load_dataset()
model1 = UserVectorGNN(input_size=200,output_size=200)
# model = model1.to(device)
model2 = VGAE(VariationalGCNEncoder(input_size=200,output_size=200))
model = model2.to(device)
# loss_function = L1Loss()
optimizer = AdamW(model.parameters(), lr=0.001)
loss = 0
for e in range(epoch):
    model.train()
    optimizer.zero_grad()
    z = model.encode(dataset.x, dataset.edge_index)
    recon_loss = model.recon_loss(z, dataset.pos_edge_label_index)
    kl_loss = (1 / dataset.num_nodes) * model.kl_loss()
    loss = recon_loss + kl_loss
    loss.backward()
    optimizer.step()