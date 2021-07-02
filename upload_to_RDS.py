import psycopg2
import pandas as pd
import csv

with open("db_creds.txt", "r") as file:
    user, password, host, port = file.read().split(",")
conn = psycopg2.connect(database="", user=user, password=password, host=host, port=port)

cur = conn.cursor()
cur.execute("SELECT * FROM urls_to_scrape")
print(cur.fetchall())
try:
    conn = psycopg2.connect(
    database="",
    user=user,
    password=password,
    host=host,
    port=port
    )
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS properties 
    (index NUMERIC
    country varchar
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