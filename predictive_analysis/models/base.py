from sklearn.model_selection import GridSearchCV
from sklearn.metrics import *
import time
import torch

class BaseModel:
    def __init__(self, X, y) -> None:
        self.X = X
        self.y = y
        self.tune()
        
    def tune(self):
        """ Turns hyperparameters of the model. """
        tuning_start = time.time()
        grid_search = GridSearchCV(estimator=self.model, param_grid=self.hyperparameters)
        grid_search.fit(X=self.X, y=self.y)
        tuning_end = time.time()

        self.tuning_time = tuning_end - tuning_start
        self.best_model = grid_search.best_estimator_
        self.best_hyperparameters = grid_search.best_params_
        self.fitting_time = grid_search.refit_time_

    def score(self, X_sets, y_sets):
        """ Returns the score of the tuned model for every set of the data. """
        self.scores = {"accuracy": {}, "f1": {}, "log_loss": {}}
        y_pred_sets = {}
        for set in range(len(X_sets)):
            y_pred_sets[set] = self.best_model.predict(X_sets[set])
            self.scores["accuracy"][set] = accuracy_score(y_sets[set], y_pred_sets[set])
            self.scores["f1"][set] = f1_score(y_sets[set], y_pred_sets[set])
            self.scores["cross_entropy"][set] = log_loss(y_sets[set], y_pred_sets[set])

class ModelSelector:
    def __init__(self, models, X, y) -> None:
        self.models = {model.__name__: model(X, y) for model in models}

    
    def get_best_model(self, X_sets, y_sets):
        max_score = 0
        for key in self.models.keys():
            self.models[key].score(X_sets, y_sets)

            if self.models[key].scores["accuracy"][1] > max_score:
                max_score = self.models[key].scores["accuracy"][1]
                self.best_model_name = key
                self.best_model_params = self.models[key].best_hyperparameters
                self.best_model = self.models[key].best_model
        
        print(self.best_model_params)
            
class BaseNetwork(torch.nn.Module):
    """
    Abstract class for Neural Network model.
    implemented from torch.nn.Module.
    Only accepts numerical features.

    Must implement:
    - layers attribute
    - get_loss method
    
    Methods created to match the ones used by Sci-kit Learn models.
    """
    def __init__(self):
        super().__init__()
        
    def forward(self, X):
        """
        Predicts the value of an output for each row of X
        using the model.
        """
        return self.layers(X)