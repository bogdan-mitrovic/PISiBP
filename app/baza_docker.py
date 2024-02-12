import psycopg2
import json
import random
from datetime import datetime, timedelta

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='db',
    port='5432'
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

kategorije = ["politika", "crna hronika", "razonoda", "sport", "obrazovanje", "skandal"]
for cat in kategorije:
    cur.execute(
                "INSERT INTO news_category (name) VALUES (%s)",
                (cat,)
            )

i = 0

# Insert data from 'data_world_example.json'
with open('data_world_example.json', 'r') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<6 else 1
        likes = random.randint(0, 324)
        dislikes = random.randint(0, 24)
        low = likes + dislikes
        views = random.randint(low, low + 145)
        cur.execute(
            "INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item["title"], item["raw_content"], item["news_post_date"], item["header_image"], views, likes, dislikes, i)
        )

# Insert data from 'cnn_data.json'
with open('cnn_data.json', 'r') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<6 else 1
        likes = random.randint(0, 324)
        dislikes = random.randint(0, 24)
        low = likes + dislikes
        views = random.randint(low, low + 145)
        cur.execute(
            "INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item["title"], item["raw_content"], item["published_at"], item["header_image"], views, likes, dislikes, i)
        )

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
