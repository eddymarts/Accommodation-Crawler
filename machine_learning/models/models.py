from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from base import BaseModel

class LinearRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = LinearRegression()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class KNNRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = KNeighborsRegressor()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class DTRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = DecisionTreeRegressor()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class RFRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = RandomForestRegressor()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)
    
class SVRegressor(BaseModel):
    def __init__(self, X, y) -> None:
        self.model = SVR()
        self.hyperparameters = {'fit_intercept': [True, False], 
                                'normalize': [True, False]}
        super().__init__(X, y)