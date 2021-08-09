import pandas as pd
from pprint import pprint
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
X, y = properties.load_reg(category='sale', return_X_y=True)
analyse(X)
analyse(y)