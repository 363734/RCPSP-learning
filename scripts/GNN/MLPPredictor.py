import torch.nn as nn
import torch
import torch.nn.functional as F


class MLPPredictor(nn.Module):  # same as edgeDecoder
    def __init__(self, h_feats):
        super().__init__()
        self.W1 = nn.Linear(h_feats * 2, h_feats)
        self.W2 = nn.Linear(h_feats, 1)

    def apply_edges(self, edges):
        """
        Computes a scalar score for each edge of the given graph.

        Parameters
        ----------
        edges :
            Has three members ``src``, ``dst`` and ``data``, each of
            which is a dictionary representing the features of the
            source nodes, the destination nodes, and the edges
            themselves.

        Returns
        -------
        dict
            A dictionary of new edge features.
        """
        h = torch.cat([edges.src['h'], edges.dst['h']], 1)

        return {'score': self.W2(F.relu(self.W1(h))).squeeze(1)}

        # a = self.W1(h)
        # b = F.relu(a)
        # c = self.W2(b)
        # d = c.squeeze(1)
        # return {'score': d}

    def forward(self, g, h):
        with g.local_scope():
            g.ndata['h'] = h
            g.apply_edges(self.apply_edges)
            return g.edata['score']
