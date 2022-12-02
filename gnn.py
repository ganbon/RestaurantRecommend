from torch_geometric.nn import GCNConv
import torch

class VaritationGCNEncoder(torch.nn.Module):
    def __init__(self,input_size,output_size):
        super.__init__()
        self.conv1 = GCNConv(input_size,output_size*2)
        self.conv_mu = GCNConv(output_size*2,output_size)
        self.conv_logsted = GCNConv(output_size*2,output_size)
        