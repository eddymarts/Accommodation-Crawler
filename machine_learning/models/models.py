from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from models.base import BaseModel

class LinearRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = LinearRegression()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class KNNRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = KNeighborsRegressor()
        self.hyperparameters = {'n_neighbors': list(range(1, 10)), 
                                'weights': ['uniform', 'distance'],
                                }
        super().__init__(X, y)
    
class DTRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = DecisionTreeRegressor()
        self.hyperparameters = {'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)]}
        super().__init__(X, y)
    
class RFRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = RandomForestRegressor()
        self.hyperparameters = {'n_estimators': [num*10 for num in range(10, 11)],
                                'min_samples_split': list(range(2, 4)), 
                                'min_samples_leaf': list(range(1, 3)),
                                'min_weight_fraction_leaf': [num/10 for num in range(2)]}
        super().__init__(X, y)
    
class SVRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = SVR()
        self.hyperparameters = {#'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], 
                                'degree': list(range(2, 10)),
                                'gamma': ['scale', 'auto'],
                                'coef0': list(range(100)),
                                'C': [num/1 for num in range(10)],
                                'epsilon': [num/100 for num in range(10)],
                                'shrinking': [False, True]}
        super().__init__(X, y)

class ANNRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = MLPRegressor()
        self.hyperparameters = {'hidden_layer_sizes': [(100, 100, 100, 100, 100)],
                                #'activation': ['identity', 'logistic', 'tanh', 'relu'],
                                #'alpha': [num/10000 for num in range(1, 100)],
                                'max_iter': [1000]}
        super().__init__(X, y)