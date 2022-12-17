from pymongo import MongoClient
import psycopg2

mongo_client = MongoClient("mongodb+srv://handoyo:1826@cluster0.wnfttz9.mongodb.net")

mongodb_zips = [item for item in mongo_client.sample_training.zips.find()]

data_list = []
for item in mongodb_zips:
    _id = str(item['_id'])
    city = item['city']
    zip = item['zip']
    loc_x = item['loc']['x']
    loc_y = item['loc']['y']
    pop = item['pop']
    state = item['state']
    del item['loc']
    data_list.append((_id, city, zip, loc_x, loc_y, pop, state))

# Connect to the database
conn = psycopg2.connect(host='postgres-de9', port='5432', database='postgres', user='postgres', password='admin')
#conn = psycopg2.connect(host='localhost', port='5445', database='postgres', user='postgres', password='admin')

# Create a cursor
cur = conn.cursor()

# Prepare the INSERT statement
insert_stmt = "INSERT INTO zips (_id, city, zip, loc_x, loc_y, pop, state) VALUES (%s, %s, %s, %s, %s, %s, %s)"

print(data_list)
# Execute the INSERT statement with the data
cur.executemany(insert_stmt, data_list)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
conn.close()


