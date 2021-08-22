import torch
import torch.nn.functional as F
import numpy as np
from base import BaseNetwork

class LinearRegression(BaseNetwork):
    """
    Class representing Linear Regression predicting model
    implemented from Abstract class BaseNetwork.
    Only accepts numerical features.
    
    Methods created to match the ones used by Sci-kit Learn models.
    """
    def __init__(self, n_features, n_labels):
        super().__init__()
        self.layers = torch.nn.Linear(n_features, n_labels)

class BinaryLogisticRegression(LinearRegression):
    """
    Class representing Binary Logistic Regression predicting model
    implemented from the Linear Regression model.
    Only accepts numerical features.
    
    Methods created to match the ones used by Sci-kit Learn models.
    """
    def __init__(self, n_features, n_labels):
        super().__init__(n_features, n_labels)
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(n_features, n_labels), 
            torch.nn.Sigmoid())

class LogisticRegression(BinaryLogisticRegression):
    """
    Class representing Multiclass Logistic Regression predicting model
    implemented from the Linear Regression model.
    Only accepts numerical features.
    
    Methods created to match the ones used by Sci-kit Learn models.
    """
    def __init__(self, n_features, n_labels):
        super().__init__(n_features, n_labels)
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(n_features, n_labels), 
            torch.nn.Softmax(1))