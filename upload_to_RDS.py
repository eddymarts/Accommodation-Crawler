import psycopg2
import sys
import boto3
import os

ENDPOINT="zoopla-primelocation-properties-db.cjp3g463xyzn.eu-west-2.rds.amazonaws.com"
PORT="5432"
USR="postgres"
PWORD="properties-scraper"
REGION="eu-west-2c"
DBNAME="zoopla-primelocation-properties-db"

#gets the credentials from .aws/credentials
# session = boto3.Session(profile_name='')
# client = session.client('rds')

# token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PWORD)
    cur = conn.cursor()
    cur.execute(""""CREATE TABLE IF NOT EXISTS properties 
    (index NUMERIC
    country text
    city text
    address text
    post_code text
    longitude NUMERIC
    latitude NUMERIC

    area_m_2 NUMERIC
    number_of_bedrooms NUMERIC
    number_of_bathrooms NUMERIC

    is_rental Boolean
    is_shared_accomodation Boolean
    is_student Boolean
    is_furnished Boolean

    price_for_sale NUMERIC
    price_per_month_gbp NUMERIC

    property_type TEXT

    url TEXT
    description TEXT
    agency TEXT
    agency_phone_number TEXT
    google_maps TEXT
    pictures TEXT

    updated_date = Datetime""")
    cur.commit()
    cur.execute("""
    COPY properties(index,
    country,
    city,
    address,
    post_code,
    longitude,
    latitude,

    area_m_2,
    number_of_bedrooms,
    number_of_bathrooms,

    is_rental,
    is_shared_accomodation,
    is_student,
    is_furnished,

    price_for_sale,
    price_per_month_gbp,

    property_type,

    url,
    description,
    agency,
    agency_phone_number,
    google_maps,
    pictures,)
    FROM 'properties_db.csv'
    DELIMITER ','
    CSV HEADER;""")
    cur.commit()
except Exception as e:
    print("Database connection failed due to {}".format(e))