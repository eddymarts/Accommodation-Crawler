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

class CustomNetRegression(torch.nn.Module):
    def __init__(self, n_features, n_labels, num_layers=10, neuron_incr=10, 
                dropout=0.5, batchnorm=False):
        super().__init__()
        self.layers = self.get_layers(n_features, n_labels, num_layers,
                                        neuron_incr, dropout, batchnorm)
    
    def forward(self, X):
        for layer in self.layers:
            X = layer(X)
        
        return X
    
    def get_layers(n_features, n_labels, num_layers, neuron_incr, dropout, batchnorm):
        current_neurons = n_features
        layers = []

        for layer in range(num_layers):
            if layer <= round(num_layers/2):
                next_neurons = current_neurons+neuron_incr
            else:
                next_neurons = current_neurons-neuron_incr

            if batchnorm:
                layers.append(torch.nn.BatchNorm1d(current_neurons))

            layers.append(torch.nn.Linear(current_neurons, next_neurons))
            layers.append(torch.nn.ReLU())
            layers.append(torch.nn.Dropout(p=dropout))
            current_neurons = next_neurons
        
        print(current_neurons)

        if batchnorm:
            layers.append(torch.nn.BatchNorm1d(current_neurons))
        layers.append(torch.nn.Linear(current_neurons, n_labels))

        return layers

class CustomNetBiClassification(CustomNetRegression):
    def __init__(self, n_features, n_labels, num_layers=10, neuron_incr=10,
                dropout=0.5, batchnorm=False):
        super().__init__(n_features, n_labels, num_layers=num_layers,
                neuron_incr=neuron_incr, dropout=dropout, batchnorm=batchnorm)
        self.layers.append(torch.nn.Sigmoid())

class CustomNetClassification(CustomNetRegression):
    def __init__(self, n_features, n_labels, num_layers=10, neuron_incr=10,
                dropout=0.5, batchnorm=False):
        super().__init__(n_features, n_labels, num_layers=num_layers,
                neuron_incr=neuron_incr, dropout=dropout, batchnorm=batchnorm)
        self.layers.append(torch.nn.Softmax(1))

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