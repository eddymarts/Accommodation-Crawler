from sklearn.model_selection import GridSearchCV
import time

import torch
import torch.nn.functional as F
import numpy as np
from torch.utils.tensorboard import SummaryWriter

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

    def fit(self, train_load, test_load=None, optimiser=None, lr = 0.001, epochs=1000,
            acceptable_error=0.001, return_loss=False):
        """
        Optimises the model parameters for the given data.

        INPUTS: train_load -> torch.utils.data.DataLoader object with the data.
                lr -> Learning Rate of Mini-batch Gradient Descent.
                        default = 0.001.
                epochs -> Number of iterationns of Mini-Batch Gradient Descent.
                        default = 100
        """

        if optimiser==None:
            optimiser = torch.optim.SGD(self.parameters(), lr=lr)

        writer = SummaryWriter()

        mean_train_loss = []
        mean_validation_loss = []
        
        tuning_start = time.time()
        for epoch in range(epochs):
            training_loss = []
            self.train()
            for X_train, y_train in train_load:
                optimiser.zero_grad()
                y_hat = self.forward(X_train)
                train_loss = self.get_loss(y_hat, y_train)
                training_loss.append(train_loss.item())
                train_loss.backward()
                optimiser.step()
            
            mean_train_loss.append(np.mean(training_loss))
            writer.add_scalar("./loss/train", mean_train_loss[-1], epoch)
            
            if test_load:
                validation_loss = []
                self.eval() # set model in inference mode (need this because of dropout)
                for X_val, y_val in test_load:
                    y_hat_val = self.forward(X_val)
                    val_loss = self.get_loss(y_hat_val, y_val)
                    validation_loss.append(val_loss.item())
                mean_validation_loss.append(np.mean(validation_loss))
                writer.add_scalar("./loss/validation", mean_validation_loss[-1], epoch)

                if epoch > 2 and (
                    (abs(mean_validation_loss[-2]- mean_validation_loss[-1])/mean_validation_loss[-1] < acceptable_error)
                    or (mean_validation_loss[-1] > mean_validation_loss[-2])):
                    print(f"Validation train_loss for epoch {epoch} is {mean_validation_loss[-1]}")
                    break
        
        tuning_end = time.time()
        writer.close()
        if return_loss:
            return {'training': mean_train_loss,
                    'validation': mean_validation_loss,
                    'fit_time': tuning_end - tuning_start}
        
    def predict(self, data_load, return_y=False):
        """
        Predicts the value of an output for each row of X
        using the fitted model.

        X is the data from data_load (DataLoader object).

        Returns the predictions.
        """
        self.eval()
        for idx, (X_val, y_val) in enumerate(data_load):
            if idx == 0:
                y_hat_val = self(X_val)
                y_label = y_val
            else:
                y_hat_val = torch.cat((y_hat_val, self(X_val)), dim=0)
                y_label = torch.cat((y_label, y_val), dim=0)
        
        if return_y:
            return y_label.reshape(-1, 1), y_hat_val
        else:
            return y_hat_val

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
        
        print(self.best_model_params)
            

    

