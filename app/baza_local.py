import sqlite3
import json
import random
from datetime import datetime, timedelta
from collections import Counter
from django.utils import timezone
import re
from django.conf import settings

settings.configure()

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

datum = timezone.make_aware(datetime.now())

# Insert categories
kategorije = ["politika","nauka", "razonoda",  "obrazovanje", "sport", "crna hronika"]
for cat in kategorije:
    cur.execute("INSERT INTO news_category (name) VALUES (?)", (cat,))
conn.commit()

cur.execute("INSERT INTO auth_user (password, is_superuser, username, email, is_staff, is_active, first_name, last_name, date_joined) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ("pbkdf2_sha256$260000$6oFRDI3och2qqeMrgKNSi7$1ofwwY49lKQ3D/GVrCwfWwdnKymYA9VOC1qpSOnzZDU=",1,"pantelija","pantelija@gmail.com",1,1,"Nenad","Pantelic",datum))

cur.execute("SELECT id FROM django_content_type WHERE app_label='news' AND model='news'")
content_type_id = cur.fetchone()[0]

def get_most_repeated_words(content):
    words = re.findall(r'\b\w{4,}\b', content.lower())
    word_counts = Counter(words)
    ignored_words={
    'about', 'after', 'all', 'also', 'am', 'an', 'and', 'another', 'any', 'are', 'around', 'as', 
    'at', 'away', 'back', 'be', 'because', 'been', 'before', 'being', 'between', 'both', 'but', 
    'by', 'came', 'can', 'come', 'could', 'day', 'did', 'do', 'does', 'even', 'first', 'for', 
    'found', 'get', 'give', 'go', 'good', 'great', 'had', 'has', 'have', 'he', 'her', 'here', 'him',
    'himself', 'his', 'how', 'however', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'like', 'look',
    'made', 'make', 'many', 'me', 'might', 'more', 'most', 'much', 'must', 'my', 'never', 'no', 'not',
    'now', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'out', 'over', 'said', 'same',
    'see', 'should', 'since', 'so', 'some', 'still', 'such', 'take', 'than', 'that', 'the', 'their',
    'them', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
    'up', 'use', 'very', 'want', 'way', 'we', 'well', 'were', 'what', 'when', 'where', 'which',
    'while', 'who', 'why', 'will', 'with', 'would', 'you', 'your', 'yet', 'you', 'yours', 'yourself'
}


    for word in ignored_words:
        if word in word_counts:
            del word_counts[word]
    most_common_words = word_counts.most_common(3)
    return [word for word, _ in most_common_words]




i=0






# Insert data from 'Latest_News.json'
with open('baze.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<5 else 1
        datum = datum if i<5 else (datum- timedelta(days=1))

        likes = random.randint(220,324)
        dislikes = random.randint(50,74)
        low = 500
        views = random.randint(low, low + 145)
        cur.execute("INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item["title"], item["raw_content"], datum ,item["header_image"], views, likes, dislikes, item["cat"]))

        # Retrieve the ID of the news item that was just inserted
        news_id = cur.lastrowid
        # Create tags and associate them with the News object
        for tag_name in item.get("tags", []):
            # Check if the tag already exists
            cur.execute(
                "SELECT id FROM taggit_tag WHERE name = ?",
                (tag_name,)
            )
            existing_tag = cur.fetchone()
            if existing_tag:
                tag_id = existing_tag[0]
            else:
                # If tag doesn't exist, insert it
                cur.execute(
                    "INSERT INTO taggit_tag (name, slug) VALUES (?, ?)",
                    (tag_name, tag_name)
                )
                tag_id = cur.lastrowid

            # Insert tagged item
            cur.execute(
                "SELECT 1 FROM taggit_taggeditem WHERE content_type_id = ? AND object_id = ? AND tag_id = (SELECT id FROM taggit_tag WHERE name = ?)",
                (content_type_id, news_id, tag_name)
            )
            existing_tagged_item = cur.fetchone()
            if not existing_tagged_item:
                # Insert tagged item
                cur.execute(
                    "INSERT INTO taggit_taggeditem (content_type_id, object_id, tag_id) VALUES (?, ?, (SELECT id FROM taggit_tag WHERE name = ?))",
                    (content_type_id, news_id, tag_name)
                )












i=0






# Insert data from 'Latest_News.json'
with open('cnn_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<5 else 1
        datum = datum if i<5 else (datum- timedelta(days=1))

        likes = random.randint(0,324)
        dislikes = random.randint(0,24)
        low = likes + dislikes
        views = random.randint(low, low + 145)
        cur.execute("INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item["title"], item["raw_content"], datum ,item["header_image"], views, likes, dislikes, random.randint(1,6)))

        # Retrieve the ID of the news item that was just inserted
        news_id = cur.lastrowid
        tagovi = get_most_repeated_words(item["content"])
        # Create tags and associate them with the News object
        for tag_name in tagovi:
            # Check if the tag already exists
            cur.execute(
                "SELECT id FROM taggit_tag WHERE name = ?",
                (tag_name,)
            )
            existing_tag = cur.fetchone()
            if existing_tag:
                tag_id = existing_tag[0]
            else:
                # If tag doesn't exist, insert it
                cur.execute(
                    "INSERT INTO taggit_tag (name, slug) VALUES (?, ?)",
                    (tag_name, tag_name)
                )
                tag_id = cur.lastrowid

            # Insert tagged item
            cur.execute(
                "SELECT 1 FROM taggit_taggeditem WHERE content_type_id = ? AND object_id = ? AND tag_id = (SELECT id FROM taggit_tag WHERE name = ?)",
                (content_type_id, news_id, tag_name)
            )
            existing_tagged_item = cur.fetchone()
            if not existing_tagged_item:
                # Insert tagged item
                cur.execute(
                    "INSERT INTO taggit_taggeditem (content_type_id, object_id, tag_id) VALUES (?, ?, (SELECT id FROM taggit_tag WHERE name = ?))",
                    (content_type_id, news_id, tag_name)
                )









with open('huffpost_news_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<5 else 1
        datum = datum if i<5 else (datum- timedelta(days=1))
        likes = random.randint(0, 324)
        dislikes = random.randint(0, 24)
        low = likes + dislikes
        views = random.randint(low, low + 145)
        cur.execute(
            "INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (item["headline"], item["raw_description"], datum , item["primary_image"], views, likes, dislikes, random.randint(1,6))
        )

        news_id = cur.lastrowid
        tagovi = get_most_repeated_words(item["description"])
        # Create tags and associate them with the News object
        for tag_name in tagovi:
            # Check if the tag already exists
            cur.execute(
                "SELECT id FROM taggit_tag WHERE name = ?",
                (tag_name,)
            )
            existing_tag = cur.fetchone()
            if existing_tag:
                tag_id = existing_tag[0]
            else:
                # If tag doesn't exist, insert it
                cur.execute(
                    "INSERT INTO taggit_tag (name, slug) VALUES (?, ?)",
                    (tag_name, tag_name)
                )
                tag_id = cur.lastrowid

            # Insert tagged item
            cur.execute(
                "SELECT 1 FROM taggit_taggeditem WHERE content_type_id = ? AND object_id = ? AND tag_id = (SELECT id FROM taggit_tag WHERE name = ?)",
                (content_type_id, news_id, tag_name)
            )
            existing_tagged_item = cur.fetchone()
            if not existing_tagged_item:
                # Insert tagged item
                cur.execute(
                    "INSERT INTO taggit_taggeditem (content_type_id, object_id, tag_id) VALUES (?, ?, (SELECT id FROM taggit_tag WHERE name = ?))",
                    (content_type_id, news_id, tag_name)
                )





with open('data_world_example.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for item in data:
        i = i+1 if i<5 else 1
        datum = datum if i<5 else (datum- timedelta(days=1))
        likes = random.randint(0, 324)
        dislikes = random.randint(0, 24)
        low = likes + dislikes
        views = random.randint(low, low + 145)
        cur.execute(
            "INSERT INTO news_news (title, content, publish_date, image, views, likes, dislikes, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (item["title"], item["raw_content"], datum, item["header_image"], views, likes, dislikes, random.randint(1,6))
        )

        news_id = cur.lastrowid
        tagovi = get_most_repeated_words(item["content"])
        # Create tags and associate them with the News object
        for tag_name in tagovi:
            # Check if the tag already exists
            cur.execute(
                "SELECT id FROM taggit_tag WHERE name = ?",
                (tag_name,)
            )
            existing_tag = cur.fetchone()
            if existing_tag:
                tag_id = existing_tag[0]
            else:
                # If tag doesn't exist, insert it
                cur.execute(
                    "INSERT INTO taggit_tag (name, slug) VALUES (?, ?)",
                    (tag_name, tag_name)
                )
                tag_id = cur.lastrowid

            # Insert tagged item
            cur.execute(
                "SELECT 1 FROM taggit_taggeditem WHERE content_type_id = ? AND object_id = ? AND tag_id = (SELECT id FROM taggit_tag WHERE name = ?)",
                (content_type_id, news_id, tag_name)
            )
            existing_tagged_item = cur.fetchone()
            if not existing_tagged_item:
                # Insert tagged item
                cur.execute(
                    "INSERT INTO taggit_taggeditem (content_type_id, object_id, tag_id) VALUES (?, ?, (SELECT id FROM taggit_tag WHERE name = ?))",
                    (content_type_id, news_id, tag_name)
                )












     
conn.commit()
cur.close()
conn.close()
