from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from models.base import BaseModel

class LogisticRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = LogisticRegression()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class KNNClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = KNeighborsClassifier()
        self.hyperparameters = {'n_neighbors': list(range(1, 10)), 
                                'weights': ['uniform', 'distance'],
                                }
        super().__init__(X, y)
    
class DTClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = DecisionTreeClassifier()
        self.hyperparameters = {'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)]}
        super().__init__(X, y)
    
class RFClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = RandomForestClassifier()
        self.hyperparameters = {'n_estimators': [num*10 for num in range(10, 11)],
                                'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)]}
        super().__init__(X, y)
    
class SVClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = SVC()
        self.hyperparameters = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], 
                                'degree': list(range(2, 10)),
                                'gamma': ['scale', 'auto'],
                                'coef0': list(range(100)),
                                'C': [num/1 for num in range(10)],
                                'epsilon': [num/100 for num in range(10)],
                                'shrinking': [False, True]}
        super().__init__(X, y)

class ANNClassifier(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = MLPClassifier()
        self.hyperparameters = {'hidden_layer_sizes': [(100, 100, 100, 100, 100)],
                                'activation': ['identity', 'logistic', 'tanh', 'relu'],
                                'alpha': [num/10000 for num in range(1, 100)],
                                'max_iter': [1000]}
        super().__init__(X, y)