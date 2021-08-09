from sklearn.model_selection import GridSearchCV
import time

class BaseModel:
    def __init__(self, X, y) -> None:
        self.X = X
        self.y = y
        self.tune()
        
    
    def tune(self):
        """ Turns hyperparameters of the model. """
        tuning_start = time.time()
        grid_search = GridSearchCV(estimator=self.model, param_grid=self.hyperparameters)
        grid_search.fit(self.X, self.y)
        tuning_end = time.time()

        self.tuning_time = tuning_end - tuning_start
        self.best_model = grid_search.best_estimator_
        self.best_hyperparameters = grid_search.best_params_
        self.fitting_time = grid_search.refit_time_