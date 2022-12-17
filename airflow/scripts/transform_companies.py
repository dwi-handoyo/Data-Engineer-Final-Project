from pymongo import MongoClient

import psycopg2

mongo_client = MongoClient("mongodb+srv://handoyo:1826@cluster0.wnfttz9.mongodb.net")

mongodb_companies = [item for item in mongo_client.sample_training.companies.find()]

data_list = []
for item in mongodb_companies:

    _id = str(item['_id'])
    name = item['name']
    permalink = item['permalink']
    crunchbase_url = item['crunchbase_url']
    homepage_url = item['homepage_url']
    blog_url = item['blog_url']
    blog_feed_url = item['blog_feed_url']
    twitter_username = item['twitter_username']
    category_code = item['category_code']
    number_of_employees = item['number_of_employees']
    founded_year = item['founded_year']
    founded_month = item['founded_month']
    founded_day = item['founded_day']
    deadpooled_year = item['deadpooled_year']
    tag_list = item['tag_list']
    alias_list = item['alias_list']
    email_address = item['email_address']
    phone_number = item['phone_number']
    description = item['description']
    created_at = item['created_at']
    updated_at = item['updated_at']
    overview = item['overview']
    if item['offices'] == []:
        offices_description = None
        offices_address1 = None
        offices_address2 = None
        offices_zip_code = None
        offices_city = None
        offices_state_code = None
        offices_country_code = None
        offices_latitude = None
        offices_longitude = None
    else:
        offices_description = item['offices'][0]['address1']
        offices_address1 = item['offices'][0]['address1']
        offices_address2 = item['offices'][0]['address2']
        offices_zip_code = item['offices'][0]['zip_code']
        offices_city = item['offices'][0]['city']
        offices_state_code = item['offices'][0]['state_code']
        offices_country_code = item['offices'][0]['country_code']
        offices_latitude = item['offices'][0]['latitude']
        offices_longitude = item['offices'][0]['longitude']
    
    data_list.append((_id, name, permalink, crunchbase_url, homepage_url, blog_url, blog_feed_url, twitter_username, \
    category_code, number_of_employees, founded_year, founded_month, founded_day, deadpooled_year, \
    tag_list, alias_list, email_address, phone_number, description, created_at, updated_at, overview, \
    offices_description, offices_address1, offices_address2, offices_zip_code, offices_city, offices_state_code, \
    offices_country_code, offices_latitude, offices_longitude))


# Connect to the database
conn = psycopg2.connect(host='postgres-de9', port='5432', database='postgres', user='postgres', password='admin')
#conn = psycopg2.connect(host='localhost', port='5445', database='postgres', user='postgres', password='admin')

# Create a cursor
cur = conn.cursor()

# Prepare the INSERT statement
insert_stmt = "INSERT INTO companies (_id, name, permalink, crunchbase_url, homepage_url, blog_url, blog_feed_url, \
            twitter_username, category_code, number_of_employees, founded_year, founded_month, founded_day, \
            deadpooled_year, tag_list, alias_list, email_address, phone_number, description, created_at, updated_at, \
            overview, offices_description, offices_address1, offices_address2, offices_zip_code, offices_city, \
            offices_state_code, offices_country_code, offices_latitude, offices_longitude ) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s)"

print(data_list)
# Execute the INSERT statement with the data
cur.executemany(insert_stmt, data_list)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
conn.close()
