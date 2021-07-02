import psycopg2

#Connecting to sqlite
with open("db_creds.txt", "r") as file:
    user, password, host, port = file.read().split(",")
conn = psycopg2.connect(database="", user=user, password=password, host=host, port=port)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("DROP TABLE urls_to_scrape")
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

# cursor.execute("""UPDATE urls_to_scrape
# SET scraped_yet = False;""")

# #Commit your changes in the database
# conn.commit()

# cursor.execute("DROP TABLE properties")
# print("Table dropped... ")

#Commit your changes in the database
# conn.commit()

#Closing the connection
conn.close()