import sqlite3
import pandas as pd
from pprint import pprint

def print_df(df, max_rows=6, max_columns=None):
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):  # more options can be specified also
        pprint(df)

def describe_df(df, max_columns=None):
    with pd.option_context('display.max_columns', max_columns):  # more options can be specified also
        print(df.describe())

def get_furnished(description: str) -> bool:
        """
        Returns whether it is funished:
        INPUT: all_details: list of strings, All details of the property

        OUTPUT:
            is_furnish: bool
        """
        description = description.lower()

        if "unfurnished" in description or "no furnished" in description:
            is_furnish = False
        elif "furnished" in description:
            is_furnish = True
        else:
            is_furnish = None

        return is_furnish

# Connecting to sqlite
pl_db = sqlite3.connect('property_db.sqlite3')

#Creating a cursor object using the cursor() method
pl_cursor = pl_db.cursor()

pl_cursor.execute("SELECT * FROM properties")
pl_column_names = [column[0] for column in pl_cursor.description]
PrimeLocation = pl_cursor.fetchall()

#Closing the connection
pl_db.close()

#Connecting to sqlite
z_db = sqlite3.connect('property_db_old_schema.sqlite3')

#Creating a cursor object using the cursor() method
z_cursor = z_db.cursor()

z_cursor.execute("SELECT * FROM properties")
z_column_names = [column[0] for column in z_cursor.description]
Zoopla = z_cursor.fetchall()

#Closing the connection
z_db.close()

# Already cleaned
PrimeLocation = pd.DataFrame(PrimeLocation, columns=pl_column_names)

# Cleaning
Zoopla = pd.DataFrame(Zoopla, columns=z_column_names)
Zoopla.drop(["long_lat", "area_m_2"], axis=1, inplace=True)

# Joint dataset
Properties = pd.concat([PrimeLocation, Zoopla], ignore_index=True)
Properties.dropna(how='all', inplace = True)
Properties["id"] = Properties.index
Properties.set_index("id", inplace=True)
Properties["country"] = "United Kingdom"
Properties["city"] = Properties["address"].apply(lambda x: x.split(", ")[-1].split()[0])
Properties["is_furnished"] = Properties["description"].apply(get_furnished)
Properties["is_shared"] = Properties["description"].apply(lambda x: "shared" in x)
Properties["is_student"] = Properties["description"].apply(
    lambda x: not ("no student" in x or "not for student" in x))

# Already string
# for column in ["country", "city", "address", "post_code", "property_type", "url",
#     "description", "agency", "agency_phone_number", "google_maps", "pictures"]:
#     Properties[column] = Properties[column].astype(str)

for column in ["country", "city", "address", "post_code", 
    "property_type", "agency", "agency_phone_number"]:
    Properties[column] = Properties[column].astype('category')

for column in ["is_rental", "is_shared_accomodation", "is_student"]:
    Properties[column] = Properties[column].astype(bool)

Properties["updated_date"] = pd.to_datetime(Properties["updated_date"])
Properties["is_furnished"] = ~(~ Properties["is_rental"] & Properties["is_furnished"].isnull())
Properties.loc[Properties["area_sqft"]==0, "area_sqft"] = None
Properties.to_csv("properties_db.csv")

# setting up the db
user = 'postgres' 
password = 'postgres' 
host = 'localhost' 
port = '5432' 
db_name = 'postgres' 
db_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}" 
​
with open("db_creds.txt", "r") as file:
    user, password, host, port = file.read().split(",")
conn = psycopg2.connect(database="", user=user, password=password, host=host, port=port)
# create engine
db = create_engine(db_string) 
​
# open json file
with open('vets.json') as f:
    df = pd.read_json(f, orient='records')
​
# insert data to db
df.to_sql('vets', db)

class PropertyCleaning:
    """ Class for the process of cleaning property data. """

    def __init__(self, properties) -> PropertyCleaning:
        self.properties = properties



print_df(Properties)
print(Properties.info())
describe_df(Properties)