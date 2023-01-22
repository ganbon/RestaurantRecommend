from torch_geometric.nn import GCNConv
from torch.nn import Linear
import torch.nn.functional as F
import torch

    
class VariationalGCNEncoder(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.conv1 = GCNConv(input_size, 2 * output_size)
        self.conv_mu = GCNConv(2 * output_size, output_size)
        self.conv_logstd = GCNConv(2 * output_size, output_size)

    def forward(self, x, edge_index,edge_weight):
        x = self.conv1(x, edge_index,edge_weight).relu()
        return self.conv_mu(x, edge_index,edge_weight), self.conv_logstd(x, edge_index,edge_weight)