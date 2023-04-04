import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score


def compute_loss(pos_score, neg_score):
    scores = torch.cat([pos_score, neg_score])
    labels = torch.cat([torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])])
    return F.binary_cross_entropy_with_logits(scores, labels)


def compute_auc(pos_score, neg_score):
    scores = torch.cat([pos_score, neg_score]).numpy()
    labels = torch.cat(
        [torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])]).numpy()
    return roc_auc_score(labels, scores)


def compute_f1_score(tp, fp, fn):
    return (2 * tp) / (2 * tp + fp + fn)


def compute_precision(tp, fp):
    denom = tp + fp
    if denom == 0:
        return -1
    return tp / denom


def compute_recall(tp, fn):
    denom = tp + fn
    if denom == 0:
        return -1
    return tp / denom
