from system.dataset import ShopGraphDataset
import torch
import pandas as pd
from nlptoolsjp.file_system import *


def recommend(target_data,shop_data_list,model_path=None,user_path=None,date=None):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    user_data = file_load(user_path)
    user_data = pd.concat([user_data,target_data])
    model = torch.load(model_path).to(device)
    dataset_module = ShopGraphDataset(user_data = user_data,shop_data_list = shop_data_list,date=date)
    user_len = len(dataset_module.user_name)
    target_user_index,node_feature,edge_index,edge_attr = data_package(dataset_module)
    result = predict(model,node_feature,edge_index,edge_attr)
    _,rank = torch.topk(result[target_user_index],10)
    return [shop_data_list[r-user_len] for r in rank]

def predict(model,node_feature,edge_index,edge_attr):
    z = model.encode(node_feature,edge_index,edge_attr)
    result = model.decoder.forward_all(z)
    return result

def data_package(data_module):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    target_user_index = data_module.user_name.index("A")
    dataset = data_module.load_dataset()
    node_feature = dataset.x.to(device)
    edge_index = dataset.edge_index.long().to(device)
    edge_attr = dataset.edge_attr.double().to(device)
    return target_user_index,node_feature,edge_index,edge_attr