import pandas as pd
import psycopg2
from pprint import pprint

class PropertyCleaning:
    """ Class for the process of cleaning property data. """

    def __init__(self, db) -> None:
        self.db = db
        self.get_data()

    def get_data(self):
        """ Function to get data from AWS RDS. """

        conn = psycopg2.connect(database="",
                                user=self.db.creds['user'],
                                password=self.db.creds['password'],
                                host=self.db.creds['host'],
                                port=self.db.creds['port'])
        
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM properties_raw
                        WHERE is_clean = False;""")
        column_names = [column[0] for column in cursor.description]
        self.properties = pd.DataFrame(cursor.fetchall(), columns=column_names)
        cursor.execute("""UPDATE properties_raw
                        SET is_clean = True;""")
        conn.commit()
        conn.close()
        self.properties.drop(["is_clean"], axis=1, inplace=True)
        self.properties.set_index("id", inplace=True)

    def show(self, max_rows=6, max_columns=None):
        """ Prints all columns of dataframe. """

        with pd.option_context('display.max_rows', max_rows,
                                'display.max_columns', max_columns):
            pprint(self.properties)

    def describe(self, max_columns=None):
        """ Prints describe() of all columns of dataframe. """

        with pd.option_context('display.max_columns', max_columns):
            print(self.properties.describe())
    
    def info(self):
        """ Prints dataframe.info() """

        print(self.properties.info())

    def get_city(self):
        """ Gets the city from the address. """

        self.properties["city"] = self.properties["address"].apply(
            lambda x: x.split(", ")[-1].split()[0])
    
    def analyse(self):
        """ Prints relevant information about the dataframe. """

        self.show()
        self.describe()
        self.info()

    def get_shared(self):
        """ Gets if the property is shared from the description. """

        self.properties["is_shared"] = self.properties["description"].apply(
            lambda x: "shared" in x)
    
    def get_student(self):
        """ Gets if the property is for students from the description. """
        
        self.properties["is_student"] = self.properties["description"].apply(
            lambda x: not ("no student" in x or "not for student" in x))

    def get_furnished(self):
        """
        Gets if the property is furnished from the description.
        If there is no information about furnishing and if the property is for sale,
        it is assumed that it is not furnished.
        """
        
        def is_furnished(description: str) -> bool:
                """
                Returns whether it is funished:
                INPUT: all_details: list of strings, All details of the property

                OUTPUT:
                    is_furnish: bool
                """
                description = description.lower()

                if "unfurnished" in description or "no furnished" in description or "not furnished" in description:
                    is_furnish = False
                elif "furnished" in description:
                    is_furnish = True
                else:
                    is_furnish = None

                return is_furnish
        
        self.properties["is_furnished"] = self.properties["description"].apply(is_furnished)
        self.properties["is_furnished"] = ~(
            ~ self.properties["is_rental"] & self.properties["is_furnished"].isnull())

    def get_bills(self):
        """
        Gets if the property includes bill from the description.
        If there is no information about bills and if the property is for sale,
        it is assumed that bills are not included.
        """
        
        def bills_included(description: str) -> bool:
                """
                Returns whether bills are included:
                INPUT: all_details: list of strings, All details of the property

                OUTPUT:
                    includes_bills: bool
                """
                description = description.lower()

                inclusive_strings = ["bills are inclu", "bills inclu",
                                    "services are inclu", "services included"]

                exclusive_strings = ["bills are  not inclu", "bills not inclu",
                    "no bills inclu", "services are not inclu", "services not included",
                    "no services inclu", "not include bills", "not include services",
                    "n't include bills", "n't include services"]

                includes = False
                not_includes = False

                for string in inclusive_strings:
                    includes = (string in description) or includes

                for string in exclusive_strings:
                    not_includes = (string in description) or not_includes

                if not_includes:
                    includes_bills = False
                elif includes:
                    includes_bills = True
                else:
                    includes_bills = None

                return includes_bills
        
        self.properties["includes_bills"] = self.properties["description"].apply(bills_included)
        self.properties["includes_bills"] = ~(
            ~ self.properties["is_rental"] & self.properties["includes_bills"].isnull())
            
    def object_to_string(self):
        for column in ["country", "city", "address", "post_code", "property_type", "url",
            "description", "agency", "agency_phone_number", "google_maps", "pictures"]:
            self.properties[column] = self.properties[column].astype(str)

    def object_to_category(self):
        for column in ["country", "city", "address", "post_code", 
            "property_type", "agency", "agency_phone_number"]:
            self.properties[column] = self.properties[column].astype('category')

    def object_to_bool(self):
        for column in ["is_rental", "is_shared_accomodation", "is_student"]:
            self.properties[column] = self.properties[column].astype(bool)

    def get_duplicates(self):
        subset = ["address", "latitude", "longitude"]

    def clean(self):
        """ Cleans data in the properties dataframe. """

        self.properties.loc[self.properties["area_sqft"]==0, "area_sqft"] = None
        self.properties.dropna(how='all', inplace = True)
        self.properties["updated_date"] = pd.to_datetime(self.properties["updated_date"])
        self.properties["country"] = "United Kingdom"
        self.get_city()
        self.get_shared()
        self.get_student()
        self.get_furnished()
        self.object_to_bool()
        self.object_to_string()
        # Check FAILED scrapes
            # 1. Zoopla error in address
        # If area is null, check for area in description
        # Check for missing values using missingno
        # Data Imputation

        # Check for duplicates and appropriate aggregate way of resolving them


    def upload_to_db(self):
        self.properties.to_sql('properties_clean', self.db.engine, if_exists='append')