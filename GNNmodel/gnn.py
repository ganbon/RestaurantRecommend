from torch_geometric.nn import GCNConv
from torch.nn import Linear
import torch.nn.functional as F
import torch

class UserVectorGNN(torch.nn.Module):
    def __init__(self,input_size,output_size):
        super().__init__()
        self.conv1 = GCNConv(input_size,input_size*2)
        self.conv2 = GCNConv(input_size*2,input_size*4)
        self.conv3 = GCNConv(input_size*4,input_size*8)
        self.linear1 = Linear(input_size*8,input_size*4)
        self.linear2 = Linear(input_size*4,input_size*2)
        self.linear3 = Linear(input_size*2,input_size)

    def forward(self, x, edge_index):
        out = self.conv1(x, edge_index).relu()
        out = F.relu(out)
        out = self.conv2(out, edge_index).relu()
        out = F.relu(out)
        out = self.conv3(out, edge_index).relu()
        out = F.relu(out)
        out = self.linear1(out)
        out = F.relu(out)
        out = self.linear2(out)
        out = F.relu(out)
        out = self.linear3(out)
        out = F.relu(out)
        return out
    
class VariationalGCNEncoder(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.conv1 = GCNConv(input_size, 2 * output_size)
        self.conv_mu = GCNConv(2 * output_size, output_size)
        self.conv_logstd = GCNConv(2 * output_size, output_size)

    def forward(self, x, edge_index,edge_weight):
        x = self.conv1(x, edge_index,edge_weight).relu()
        return self.conv_mu(x, edge_index,edge_weight), self.conv_logstd(x, edge_index,edge_weight)