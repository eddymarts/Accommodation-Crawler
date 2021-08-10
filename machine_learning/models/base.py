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
        grid_search.fit(X=self.X, y=self.y)
        tuning_end = time.time()

        self.tuning_time = tuning_end - tuning_start
        self.best_model = grid_search.best_estimator_
        self.best_hyperparameters = grid_search.best_params_
        self.fitting_time = grid_search.refit_time_

    def score(self, X_sets, y_sets):
        """ Returns the score of the tuned model for every set of the data. """
        self.scores = {}
        for set in range(len(X_sets)):
            self.scores[set] = self.best_model.score(X_sets[set], y_sets[set])

class ModelSelector:
    def __init__(self, models, X, y) -> None:
        self.models = {model.__name__: model(X, y) for model in models}

    
    def get_best_model(self, X_sets, y_sets):
        max_score = 0
        for key in self.models.keys():
            self.models[key].score(X_sets, y_sets)

            if self.models[key].scores[1] > max_score:
                max_score = self.models[key].scores[1]
                self.best_model_name = key
                self.best_model_params = self.models[key].best_hyperparameters
                self.best_model = self.models[key].best_model
            

    

