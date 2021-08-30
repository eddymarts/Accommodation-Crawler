import pandas as pd
from sklearn import preprocessing
from pprint import pprint

class Data:
    """ Class to represent the self.dataset. """

    def __init__(self, one_hot=False) -> None:
        self.dataset = pd.read_csv("machine_learning/dataset.csv", index_col="id")
        self.dataset.drop(axis=1, inplace=True, labels=["address","postcode",
            "country", "city", "google_maps", "agency", "agency_phone_number",
             "url", "pictures", "description", "updated_date"])
        
        if one_hot:
            self._one_hot_property_type()
    
    def _one_hot_property_type(self):
        """ Parses property type through one hot encoding. """
        oh_encoder = preprocessing.OneHotEncoder()
        oh_encoder.fit(self.dataset[["property_type"]])

        oh_type = pd.DataFrame(
            oh_encoder.transform(self.dataset[["property_type"]]).toarray(),
            columns=oh_encoder.get_feature_names([""]))
        
        for column in oh_type.columns:
            oh_type[column] = oh_type[column].astype(bool)

        self.dataset.drop(axis=1, inplace=True, labels=["property_type"])
        self.dataset = pd.concat([self.dataset, oh_type], axis=1)

    def load_class(self, category='rental', return_X_y=False):
        """ Returns the data for predicting price for rental dataset. """
        data = self.dataset[[
                    c for c in self.dataset.columns if c not in ["property_type"]] + ["property_type"]]

        if category == 'rental':
            data = data[data["is_rental"]==True]
            data = data.drop(axis=1, inplace=False, labels=["is_rental", "price_for_sale"])
            data.dropna(how='any', inplace = True)
            if return_X_y:
                return data[[
                        c for c in data.columns if c not in ["property_type"]
                        ]], data[["property_type"]]
            return data

        elif category == 'sale':
            data = data[data["is_rental"]==False]
            data = data.drop(axis=1, inplace=False, labels=["is_rental", "price_per_month_gbp"])
            data.dropna(how='any', inplace = True)
            if return_X_y:
                return data[[
                        c for c in data.columns if c not in ["property_type"]
                        ]], data[["property_type"]]
            return data

    def load_reg(self, category='rental', return_X_y=False):
        """ Returns the data for predicting price for rental dataset. """
        data = self.dataset[[
                    c for c in self.dataset.columns if c not in ["price_per_month_gbp",
                        "price_for_sale"]] + ["price_per_month_gbp", "price_for_sale"]]

        if category == 'rental':
            data = data[data["is_rental"]==True]
            data = data.drop(axis=1, inplace=False, labels=["is_rental", "price_for_sale"])
            data.dropna(how='any', inplace = True)
            if return_X_y:
                return data[[
                        c for c in data.columns if c not in ["price_per_month_gbp"]
                        ]], data[["price_per_month_gbp"]]
            return data

        elif category == 'sale':
            data = data[data["is_rental"]==False]
            data = data.drop(axis=1, inplace=False, labels=["is_rental", "price_per_month_gbp"])
            data.dropna(how='any', inplace = True)
            if return_X_y:
                return data[[
                        c for c in data.columns if c not in ["price_for_sale"]
                        ]], data[["price_for_sale"]]
            return data
    
    def show(self, max_rows=6, max_columns=None):
        """ Prints all columns of dataframe. """

        with pd.option_context('display.max_rows', max_rows,
                                'display.max_columns', max_columns):
            pprint(self.dataset)

    def describe(self, max_columns=None):
        """ Prints describe() of all columns of dataframe. """

        with pd.option_context('display.max_columns', max_columns):
            print(self.dataset.describe())
    
    def info(self):
        """ Prints dataframe.info() """

        print(self.dataset.info())
    
    def analyse(self):
        """ Prints relevant information about the dataframe. """

        self.show()
        self.describe()
        self.info()