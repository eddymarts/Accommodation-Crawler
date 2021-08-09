from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
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
        self.hyperparameters = {'min_samples_split': list(range(2, 10)), 
                                'min_samples_leaf': list(range(1, 10)),
                                'min_weight_fraction_leaf': [num/100 for num in range(51)]}
        super().__init__(X, y)
    
class RFRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = RandomForestRegressor()
        self.hyperparameters = {'n_estimators': [num*10 for num in range(1, 10)],
                                'min_samples_split': list(range(2, 10)), 
                                'min_samples_leaf': list(range(1, 10)),
                                'min_weight_fraction_leaf': [num/100 for num in range(51)]}
        super().__init__(X, y)
    
class SVRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = SVR()
        self.hyperparameters = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'], 
                                'degree': list(range(2, 10)),
                                'gamma': ['scale', 'auto'],
                                'coef0': list(range(100)),
                                'C': [num/10 for num in range(100)],
                                'epsilon': [num/100 for num in range(100)],
                                'shrinking': [False, True]}
        super().__init__(X, y)