import torch.nn as nn
import dgl.function as fn


class DotPredictor(nn.Module):
    def forward(self, g, h):  # special method then call by applying
        with g.local_scope():  # allow local tensor for value (no override of values)
            g.ndata['h'] = h
            # Compute a new edge feature named 'score' by a dot-product between the
            # source node feature 'h' and destination node feature 'h'.
            g.apply_edges(fn.u_dot_v('h', 'h', 'score'))
            # u_dot_v returns a 1-element vector for each edge so you need to squeeze it.
            return g.edata['score'][:, 0]
