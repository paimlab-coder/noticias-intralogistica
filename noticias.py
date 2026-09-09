import feedparser
from datetime import datetime

RSS_FEEDS = {
    "Supply Chain": "https://news.google.com/rss/search?q=supply+chain&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Intralogística": "https://news.google.com/rss/search?q=intralogistica&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Armazenagem": "https://news.google.com/rss/search?q=armazenagem&hl=pt-BR&gl=BR&ceid=BR:pt-419"
}

noticias_html = ""

for categoria, feed_url in RSS_FEEDS.items():

    feed = feedparser.parse(feed_url)

    for item in feed.entries[:5]:

        noticias_html += f"""
        <div style="background:white;padding:15px;margin:10px 0;border-radius:8px;">
            <h3>
                <a href="{item.link}" target="_blank">
itle}
                </a>
            </h3>

            <small>{categoria}</small>

        </div>
        """

data = datetime.now().strftime("%d/%m/%Y %H:%M")

with open("index.html", "r", encoding="utf-8") as arquivo:

    html = arquivo.read()

html = html.replace(
    "<!-- ULTIMA_ATUALIZACAO -->",
    data
)

html = html.replace(
    "<!-- NOTICIAS_AQUI -->",
    noticias_html
)

with open("index.html", "w", encoding="utf-8") as arquivo:

    arquivo.write(html)

print("Notícias atualizadas.")
