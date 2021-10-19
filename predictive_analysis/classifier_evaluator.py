import pandas as pd
from pprint import pprint
from models.dataset import NumpyDataset, TorchDataset
from models.classification_models import *
from models.base import ModelSelector
from models.get_data import Data
import glob
import pickle

properties = Data(ordinal=True)

X_rent, y_rent, labels = properties.load_class(category='rental', return_X_y=True)
X_sale, y_sale = properties.load_class(category='sale', return_X_y=True)

rent_np = NumpyDataset(X_rent, y_rent, split=True, normalize=True, seed=42)
rent_torch = {}
rent_torch_X_sets = {}
rent_torch_y_sets = {}

for set in rent_np.X_sets.keys():
    rent_torch[set] = TorchDataset(rent_np.X_sets[set], rent_np.y_sets[set])
    rent_torch_X_sets[set] = rent_torch[set].X
    rent_torch_y_sets[set] = rent_torch[set].y


simple_models = {}
simple_model_files = glob.glob("predictive_analysis/models/rent/classifiers/simple/*.pkl")
for file in simple_model_files:
    with open(file, 'rb') as f:
        simple_models[file.split("/")[-1].split(".pkl")[0]] = pickle.load(f)

neural_models = {}
neural_model_files = glob.glob("predictive_analysis/models/rent/classifiers/neural/*.pkl")
for file in neural_model_files:
    with open(file, 'rb') as f:
        neural_models[file.split("/")[-1].split(".pkl")[0]] = pickle.load(f)


rent_simple_model_selector = ModelSelector(simple_models)
rent_neural_model_selector = ModelSelector(neural_models)

rent_simple_model_selector.get_best_model(rent_np.X_sets, rent_np.y_sets)
rent_simple_model_selector.get_best_model(rent_torch_X_sets, rent_torch_y_sets)
results = {"tuning_time": {},
            "fitting_time": {},
            "accuracy": {},
            "f1_score": {}}
            # "cross_entropy": {}}

for model in simple_models.keys:
    results["tuning_time"][model] = rent_simple_model_selector.models[model].tuning_time
    results["fitting_time"][model] = rent_simple_model_selector.models[model].fitting_time
    results["accuracy"][model] = rent_simple_model_selector.models[model].scores["accuracy"][1]
    results["f1_score"][model] = rent_simple_model_selector.models[model].scores["f1"][1]
    # results["cross_entropy"][model] = rent_simple_model_selector.models[model].scores["cross_entropy"][1]

for model in neural_models.keys:
    results["tuning_time"][model] = rent_simple_model_selector.models[model].tuning_time
    results["fitting_time"][model] = rent_simple_model_selector.models[model].fitting_time
    results["accuracy"][model] = rent_simple_model_selector.models[model].scores["accuracy"][1]
    results["f1_score"][model] = rent_simple_model_selector.models[model].scores["f1"][1]
    # results["cross_entropy"][model] = rent_simple_model_selector.models[model].scores["cross_entropy"][1]

results = pd.DataFrame(results)
print(results)
results.to_csv("predictive_analysis/classifier_results.csv")

