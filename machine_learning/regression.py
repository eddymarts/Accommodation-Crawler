import pandas as pd
from pprint import pprint
from scale_split import scalesplit
from models.models import *
from models.base import ModelSelector
from get_data import Data

def show(df, max_rows=6, max_columns=None):
    """ Prints all columns of dataframe. """

    with pd.option_context('display.max_rows', max_rows,
                            'display.max_columns', max_columns):
        pprint(df)

def describe(df, max_columns=None):
    """ Prints describe() of all columns of dataframe. """

    with pd.option_context('display.max_columns', max_columns):
        print(df.describe())

def info(df):
    """ Prints dataframe.info() """

    print(df.info())

def analyse(df):
    """ Prints relevant information about the dataframe. """

    show(df)
    describe(df)
    info(df)

properties = Data()

X_rent, y_rent = properties.load_reg(category='rental', return_X_y=True)
X_sale, y_sale = properties.load_reg(category='sale', return_X_y=True)

X_rent_sets, y_rent_sets = scalesplit(X_rent, y_rent, sets=2, test_size=0.2)
X_sale_sets, y_sale_sets = scalesplit(X_sale, y_sale, sets=2, test_size=0.2)

models = [LinearRegressor, KNNRegressor, DTRegressor, RFRegressor, ANNRegressor]
# models = [DTRegressor]

rent_model_selector = ModelSelector(models, X_rent_sets[0], y_rent_sets[0])
rent_model_selector.get_best_model(X_rent_sets, y_rent_sets)
results = {"tuning_time": {},
            "fitting_time": {},
            "R_squared": {}}

for model in models:
    results["tuning_time"][model.__name__] = rent_model_selector.models[model.__name__].tuning_time
    results["fitting_time"][model.__name__] = rent_model_selector.models[model.__name__].fitting_time
    results["R_squared"][model.__name__] = rent_model_selector.models[model.__name__].scores[1]

results = pd.DataFrame(results)
print(results)
results.to_csv("machine_learning/results.csv")

