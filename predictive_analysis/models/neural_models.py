import torch
import torch.nn.functional as F
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

class NeuralNetworkRegression(LinearRegression):
    def __init__(self, n_features, n_labels):
        super().__init__(n_features, n_labels)
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(n_features, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 40),
            torch.nn.ReLU(),
            torch.nn.Linear(40, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, n_labels)
        )

class NeuralNetworkClassification(LogisticRegression):
    def __init__(self, n_features, n_labels):
        super().__init__(n_features, n_labels)
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(n_features, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 40),
            torch.nn.ReLU(),
            torch.nn.Linear(40, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, n_labels),
            torch.nn.Softmax(1)
        )

class CNNClassifier(LogisticRegression):
    def __init__(self):
        super().__init__(1, 1)
        self.layers = torch.nn.Sequential(
            torch.nn.Conv2d(1, 10, kernel_size=5),
            torch.nn.MaxPool2d(2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(10, 20, kernel_size=5),
            torch.nn.Dropout(),
            torch.nn.MaxPool2d(2),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(320, 50),
            torch.nn.ReLU(),
            torch.nn.Dropout(),
            torch.nn.Linear(50, 10),
            torch.nn.LogSoftmax(1)
        )