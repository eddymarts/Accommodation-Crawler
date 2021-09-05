import pandas as pd
from pprint import pprint
from models.dataset import NumpyDataset, TorchDataset
from models.classification_models import *
from models.base import ModelSelector
from models.get_data import Data
import pickle

properties = Data(ordinal=True)

X_rent, y_rent, labels = properties.load_class(category='rental', return_X_y=True)
X_sale, y_sale = properties.load_class(category='sale', return_X_y=True)

rent_np = NumpyDataset(X_rent, y_rent, split=True, normalize=True, seed=42)
rent_torch = TorchDataset(rent_np.X_sets[0], rent_np.y_sets[0])

simple_models = [LRClassifier, KNNClassifier, DTClassifier, RFClassifier]
neural_models = [SGDNetworkClassifier]

for simple_model in simple_models:
    model = simple_model(rent_np.X_sets[0], rent_np.y_sets[0])
    # with open(f"predictive_analysis/models/rent/classifiers/simple/{simple_model.__name__}.pkl", 'wb') as f:
    with open(f"/content/drive/MyDrive/Profesional/AiCore/Projects/Accommodation-Crawler/predictive_analysis/models/rent/classifiers/simple/{simple_model.__name__}.pkl", 'wb') as f:
        pickle.dump(model.best_model, f)
    
    results = pd.DataFrame(model.results, index=[simple_model.__name__])
    results.to_csv(f"/content/drive/MyDrive/Profesional/AiCore/Projects/Accommodation-Crawler/predictive_analysis/models/rent/classifiers/simple/{simple_model.__name__}_params.csv")

for neural_model in neural_models:
    model = neural_model(rent_torch.X, rent_torch.y)
    # with open(f"predictive_analysis/models/rent/classifiers/neural/{neural_model.__name__}.pkl", 'wb') as f:
    with open(f"/content/drive/MyDrive/Profesional/AiCore/Projects/Accommodation-Crawler/predictive_analysis/models/rent/classifiers/neural/{neural_model.__name__}.pkl", 'wb') as f:
        pickle.dump(model.best_model, f)
    
    results = pd.DataFrame(model.results, index=[neural_model.__name__])
    # results.to_csv(f"predictive_analysis/models/rent/classifiers/neural/{neural_model.__name__}_params.csv")
    results.to_csv(f"/content/drive/MyDrive/Profesional/AiCore/Projects/Accommodation-Crawler/predictive_analysis/models/rent/classifiers/neural/{neural_model.__name__}_params.csv")

