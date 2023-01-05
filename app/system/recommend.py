from system.dataset import ShopGraphDataset
import torch
from nlptoolsjp.file_system import *


def recommend(user_path,shop_data_list,model_path=None,date=None):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    user_data = file_load(user_path)
    target_shop = user_data["店名"].tolist()
    model = torch.load(model_path).to(device)
    dataset_module = ShopGraphDataset(user_data = user_data,shop_data_list = shop_data_list,date=date)
    shop_name = dataset_module.shop_name
    user_len = len(dataset_module.user_name)
    target_user_index,node_feature,edge_index,edge_attr = data_package(dataset_module)
    if target_user_index == -1:
        return []
    result = predict(model,node_feature,edge_index,edge_attr)
    _,rank = torch.topk(result[target_user_index],10)
    return [shop_data_list[r-user_len] for r in rank if shop_name[r-user_len] in target_shop or r==0]

def predict(model,node_feature,edge_index,edge_attr):
    z = model.encode(node_feature,edge_index,edge_attr)
    result = model.decoder.forward_all(z)
    return result

def data_package(data_module):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    try:
        target_user_index = data_module.user_name.index("A")
    except:
        target_user_index = -1
    dataset = data_module.load_dataset()
    node_feature = dataset.x.to(device)
    edge_index = dataset.edge_index.long().to(device)
    edge_attr = dataset.edge_attr.double().to(device)
    return target_user_index,node_feature,edge_index,edge_attr

if __name__=="__main__":
    from shop import Shop
    from nlptoolsjp.file_system import *
    shop_data = file_load("../data/shop_data_v2.json")
    SHOP_DATA = [Shop(shop_data=shop) for name,shop in shop_data.items()]
    user_data = file_load("../data/csv/user.csv")
    lunch_data = recommend(user_data,SHOP_DATA,model_path="../data/model/gnn/lunch_vgae.pth",user_path="../data/csv/user_dinner_data.csv",date="昼")
    print(lunch_data)