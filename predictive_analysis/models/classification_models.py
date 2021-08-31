from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import torch
from skorch.classifier import NeuralNetClassifier
from models.neural_models import CustomNetClassification
from models.base import BaseModel

class LogisticRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = LogisticRegression()
        self.hyperparameters = {'penalty': ["none"],
                                'l1_ratio': [0],
                                'max_iter': [1000]}
        super().__init__(X, y)
    
class KNNClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = KNeighborsClassifier()
        self.hyperparameters = {'n_neighbors': list(range(5, 20)), 
                                'weights': ['distance']}
        super().__init__(X, y)
    
class DTClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = DecisionTreeClassifier()
        self.hyperparameters = {'criterion': ["gini", "entropy"],
                                'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)]}
        super().__init__(X, y)
    
class RFClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = RandomForestClassifier()
        self.hyperparameters = {'n_estimators': [num*10 for num in range(10, 11)],
                                'criterion': ["gini", "entropy"],
                                'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)],
                                'bootstrap': [False, True],
                                'oob_score': [False, True],
                                'class_weight': ["balanced", "balanced_subsample", None],
                                'ccp_alpha': [num/10 for num in range(3)]}
        super().__init__(X, y)
    
class SVClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = SVC()
        self.hyperparameters = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 
                                'degree': list(range(2, 5)),
                                'gamma': ['scale', 'auto'],
                                'coef0': list(range(5)),
                                'C': [num/1 for num in range(10)],
                                'shrinking': [False, True],
                                'class_weight': ["balanced", None]}
        super().__init__(X, y)

class SGDNetworkClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = NeuralNetClassifier(module=CustomNetClassification,
                                        max_epochs=1000,
                                        module__n_features=11,
                                        module__n_labels=1)
        self.hyperparameters = {'batch_size': [2**batch for batch in range(4, 11)],
                                'optimizer': [torch.optim.SGD],
                                'lr': [0.0001 * 10**num for num in range(4)],
                                'optimizer__momentum': [num/10 for num in range(10)],
                                'optimizer__dampening': [num/10 for num in range(10)],
                                'optimizer__weight_decay': [0.0001 * 10**num for num in range(4)],
                                'module__num_layers': [2**num for num in range(1, 4)],
                                'module__neuron_incr': list(range(2, 4)),
                                'module__dropout': [num/10 for num in range(10)],
                                'module__batchnorm': [False, True]}
        super().__init__(X, y)

class NesterovNetworkClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = NeuralNetClassifier(module=CustomNetClassification,
                                        max_epochs=1000,
                                        module__n_features=11,
                                        module__n_labels=1)
        self.hyperparameters = {'batch_size': [2**batch for batch in range(4, 11)],
                                'optimizer': [torch.optim.SGD],
                                'lr': [0.0001 * 10**num for num in range(4)],
                                'optimizer__momentum': [num/10 for num in range(1, 10)],
                                'optimizer__weight_decay': [0.0001 * 10**num for num in range(4)],
                                'optimizer__nesterov': [True],
                                'module__num_layers': [2**num for num in range(1, 4)],
                                'module__neuron_incr': list(range(2, 4)),
                                'module__dropout': [num/10 for num in range(10)],
                                'module__batchnorm': [False, True]}
        super().__init__(X, y)

class AdamNetworkClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = NeuralNetClassifier(module=CustomNetClassification,
                                        max_epochs=1000,
                                        module__n_features=11,
                                        module__n_labels=1)
        self.hyperparameters = {'batch_size': [2**batch for batch in range(4, 11)],
                                'optimizer': [torch.optim.Adam],
                                'lr': [0.0001 * 10**num for num in range(4)],
                                'optimizer__betas': [(num1/100, num2/1000) for num1, num2 in zip(range(80, 100), range(809, 1000, 10))],
                                'optimizer__weight_decay': [0.0001 * 10**num for num in range(4)],
                                'optimizer__amsgrad': [False, True],
                                'module__num_layers': [2**num for num in range(1, 4)],
                                'module__neuron_incr': list(range(2, 4)),
                                'module__dropout': [num/10 for num in range(10)],
                                'module__batchnorm': [False, True]}
        super().__init__(X, y)