import pandas as pd
from pprint import pprint
from models.dataset import NumpyDataset
from models.classification_models import *
from models.base import ModelSelector
from models.get_data import Data

properties = Data()

X_rent, y_rent = properties.load_class(category='rental', return_X_y=True)
X_sale, y_sale = properties.load_class(category='sale', return_X_y=True)

rent_data = NumpyDataset(X_rent, y_rent, split=True, normalize=True)

# models = [LogisticRegressor, KNNClassifier, DTClassifier, RFClassifier, SVClassifier,
#         MultilayerPerceptronClassifier, SDGNetworkClassifier, AdamNetworkClassifier]
models = [LogisticRegressor]

rent_model_selector = ModelSelector(models, rent_data.X_sets[0], rent_data.y_sets[0])
rent_model_selector.get_best_model(rent_data.X_sets, rent_data.y_sets)
results = {"tuning_time": {},
            "fitting_time": {},
            "accuracy": {},
            "f1_score": {},
            "cross_entropy": {}}

for model in models:
    results["tuning_time"][model.__name__] = rent_model_selector.models[model.__name__].tuning_time
    results["fitting_time"][model.__name__] = rent_model_selector.models[model.__name__].fitting_time
    results["accuracy"][model.__name__] = rent_model_selector.models[model.__name__].scores["accuracy"][1]
    results["f1_score"][model.__name__] = rent_model_selector.models[model.__name__].scores["f1"][1]
    results["cross_entropy"][model.__name__] = rent_model_selector.models[model.__name__].scores["cross_entropy"][1]

results = pd.DataFrame(results)
print(results)
results.to_csv("predictive_analysis/classification_results.csv")

