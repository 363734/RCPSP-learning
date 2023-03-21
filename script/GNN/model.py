import os

import torch

from script.GNN.GraphNeuralNet import GraphSAGE
from script.GNN.MLPPredictor import MLPPredictor
from script.parameters import DIR_TRAINED_MODELS


def load_model(name: str, graph):
    filepath_GNN = os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(name))
    filepath_MLP = os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(name))

    model = GraphSAGE(graph.ndata['feats'].shape[1], 16)
    model.load_state_dict(torch.load(filepath_GNN))
    model.eval()

    pred = MLPPredictor(16)
    pred.load_state_dict(torch.load(filepath_MLP))
    pred.eval()
    return model, pred
