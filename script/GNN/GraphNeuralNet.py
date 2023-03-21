import torch.nn as nn
from dgl.nn import SAGEConv, GraphConv, GATConv
import torch.nn.functional as F


class GraphSAGE(nn.Module):
    def __init__(self, in_feats, h_feats):
        super(GraphSAGE, self).__init__()

        self.conv1 = SAGEConv(in_feats, h_feats, 'mean')
        self.conv2 = SAGEConv(h_feats, h_feats, 'mean')
        self.conv3 = SAGEConv(h_feats, h_feats, 'mean')
        # self.conv4 = SAGEConv(h_feats, h_feats, 'mean')

        # works but seems worse
        # self.conv1 = GraphConv(in_feats, h_feats, 'none',allow_zero_in_degree=True)
        # self.conv2 = GraphConv(h_feats, h_feats, 'none',allow_zero_in_degree=True)
        # self.conv3 = GraphConv(h_feats, h_feats, 'none',allow_zero_in_degree=True)

        # dont work, needs more modif
        # self.conv1 = GATConv(in_feats, h_feats, num_heads=8,allow_zero_in_degree=True)
        # self.conv2 = GATConv(h_feats, h_feats, num_heads=8,allow_zero_in_degree=True)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        h = F.relu(h)
        h = self.conv3(g, h)
        # h = F.relu(h)
        # h = self.conv4(g, h)
        return h

# import torch.nn as nn
# from dgl.nn import SAGEConv, GraphConv, GATConv
# import torch.nn.functional as F
#
#
# class GraphSAGE(nn.Module):
#     def __init__(self, in_feats, h_feats):
#     # def __init__(self, nb_layers: int, agg_type: str, in_feats, h_feats):
#         super(GraphSAGE, self).__init__()
#         self.nb_layers = 3
#         self.agg_type = "mean"
#         self.conv = []
#         self.conv.append(SAGEConv(in_feats, h_feats, self.agg_type))
#         for i in range(1, self.nb_layers):
#             self.conv.append(SAGEConv(h_feats, h_feats, self.agg_type))
#
#         # works but seems worse
#         # self.conv1 = GraphConv(in_feats, h_feats, 'none',allow_zero_in_degree=True)
#         # self.conv2 = GraphConv(h_feats, h_feats, 'none',allow_zero_in_degree=True)
#         # self.conv3 = GraphConv(h_feats, h_feats, 'none',allow_zero_in_degree=True)
#
#         # dont work, needs more modif
#         # self.conv1 = GATConv(in_feats, h_feats, num_heads=8,allow_zero_in_degree=True)
#         # self.conv2 = GATConv(h_feats, h_feats, num_heads=8,allow_zero_in_degree=True)
#
#     def forward(self, g, in_feat):
#         h = self.conv[0](g, in_feat)
#         for i in range(1, self.nb_layers):
#             h = F.relu(h)
#             h = self.conv[i](g, h)
#         return h
