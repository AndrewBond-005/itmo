# metrics.py
import numpy as np


def confusion_matrix(y_true, y_pred):
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    TP = int(np.sum((y_true == 1) & (y_pred == 1)))
    TN = int(np.sum((y_true == 0) & (y_pred == 0)))
    FP = int(np.sum((y_true == 0) & (y_pred == 1)))
    FN = int(np.sum((y_true == 1) & (y_pred == 0)))
    return TP, TN, FP, FN


def accuracy(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    total = TP + TN + FP + FN
    return (TP + TN) / total if total else 0.0


def precision(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    denom = TP + FP
    return TP / denom if denom else 0.0


def recall(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    denom = TP + FN
    return TP / denom if denom else 0.0


def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * p * r / (p + r) if (p + r) else 0.0


def evaluate(y_true, y_pred):
    return {
        'accuracy': accuracy(y_true, y_pred),
        'precision': precision(y_true, y_pred),
        'recall': recall(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
    }