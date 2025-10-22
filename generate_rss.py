from html import escape
from main import get_posts

posts = get_posts()
feed_items = []
for post in posts:
    item = f"""
    <item>
        <title>{escape(post["title"])}</title>
        <link>https://blog.mariusvach.com/posts/{escape(post["slug"])}</link>
        <description>{escape(post["excerpt"]) if "excerpt" in post else ""}</description>
        <pubDate>{post["date"].strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>
        <guid>https://blog.mariusvach.com/posts/{escape(post["slug"])}</guid>
    </item>
    """
    feed_items.append(item)

feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Marius Vach Blog</title>
    <link>https://blog.mariusvach.com/</link>
    <description>Blog by Marius Vach</description>
    {"".join(feed_items)}
</channel>
</rss>
"""

with open("public/feed.xml", "w", encoding="utf-8") as f:
    f.write(feed)

print("RSS feed generated at public/feed.xml")
