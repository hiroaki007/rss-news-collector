
import feedparser
import sqlite3


class Rss_News:

    def __init__(self, title, url, published):
        self.title = title 
        self.url = url
        self.published = published

    def to_dict(self):
        return{ "title": self.title, "url": self.url, "published": self.published}


news = []

feed = feedparser.parse("https://techcrunch.com/feed/")

conn = sqlite3.connect("rss_news.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            published TEXT
    )
""")
conn.commit()


for entry in feed.entries[:3]:
    rss_new = Rss_News(entry.title, entry.link, entry.published)
    news.append(rss_new)

for new in news:
    try:
        cursor.execute(
            "INSERT INTO news(title, url, published) VALUES (?, ?, ?)",
            (new.title, new.url, new.published)
        )
        conn.commit() 

        print(f"保存しました:{new.title}")
    except sqlite3.IntegrityError:
        print(f"すでに存在するためスキップします: {new.title}")


cursor.execute("SELECT * FROM news")
rows = cursor.fetchall()
for row in rows:
    print(row)
