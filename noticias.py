from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET
import html


PESQUISAS = {
    "Intralogística": "intralogística OR intralogistica",
    "Armazenagem": "armazenagem industrial",
    "Automação Logística": "automação logística",
    "Supply Chain": "supply chain Brasil",
}


def buscar_noticias():
    noticias = []
    links_encontrados = set()

    for categoria, pesquisa in PESQUISAS.items():
        termo = quote_plus(pesquisa)

        url = (
            "https://news.google.com/rss/search?"
            f"q={termo}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        )

        print(f"Consultando: {categoria}")

        requisicao = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        try:
            with urlopen(requisicao, timeout=30) as resposta:
                conteudo_xml = resposta.read()

            raiz = ET.fromstring(conteudo_xml)

            for item in raiz.findall(".//item")[:10]:
                titulo_elemento = item.find("title")
                link_elemento = item.find("link")
                data_elemento = item.find("pubDate")

                titulo = (
                    titulo_elemento.text
                    if titulo_elemento is not None
                    else "Notícia sem título"
                )

                link = (
                    link_elemento.text
                    if link_elemento is not None
                    else "#"
                )

                data = (
                    data_elemento.text
                    if data_elemento is not None
                    else "Data não informada"
                )

                if link in links_encontrados:
                    continue

                links_encontrados.add(link)

                noticias.append({
                    "categoria": categoria,
                    "titulo": titulo,
                    "link": link,
                    "data": data,
                })

        except Exception as erro:
            print(f"Erro ao consultar {categoria}: {erro}")

    return noticias


def gerar_cards(noticias):
    if not noticias:
        return """
        <article class="card-noticia">
            <h2>Nenhuma notícia encontrada.</h2>
            <p class="data">
                Verifique a conexão e execute novamente.
            </p>
        </article>
        """

    cards = []

    for noticia in noticias:
        categoria = html.escape(noticia["categoria"])
        titulo = html.escape(noticia["titulo"])
        link = html.escape(noticia["link"], quote=True)
        data = html.escape(noticia["data"])

        card = f"""
        <article class="card-noticia">
            <span class="badge">{categoria}</span>

            <h2>
                {link}
                    {titulo}
                </a>
            </h2>

            <p class="data">Publicado em: {data}</p>
        </article>
        """

        cards.append(card)

    return "\n".join(cards)


def criar_index(noticias):
    cards = gerar_cards(noticias)
    horario = datetime.now().strftime("%d/%m/%Y às %H:%M")

    conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Radar Logístico e Intralogístico</title>

    <style>
        body {{
            font-family: "Segoe UI", Arial, sans-serif;
            background: #f4f7f6;
            color: #333;
            margin: 0;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            border-bottom: 3px solid #0056b3;
            margin-bottom: 30px;
            padding-bottom: 20px;
        }}

        h1 {{
            color: #0056b3;
        }}

        .atualizacao {{
            color: #666;
            font-size: 14px;
        }}

        .card-noticia {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 5px solid #0056b3;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.10);
        }}

        .card-noticia h2 {{
            font-size: 20px;
            line-height: 1.4;
            margin: 12px 0;
        }}

        .card-noticia a {{
            color: #222;
            text-decoration: none;
        }}

        .card-noticia a:hover {{
            color: #0056b3;
            text-decoration: underline;
        }}

        .badge {{
            display: inline-block;
            background: #0056b3;
            color: white;
            padding: 5px 9px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}

        .data {{
            color: #777;
            font-size: 13px;
        }}
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>Radar Logístico &amp; Intralogístico</h1>

            <p class="atualizacao">
                Última atualização: {horario}
            </p>
        </header>

        <main>
            {cards}
        </main>
    </div>
</body>
</html>
"""

    Path("index.html").write_text(
        conteudo,
        encoding="utf-8"
    )


if __name__ == "__main__":
    lista_noticias = buscar_noticias)

    print(f"Notícias encontradas: {len(lista_noticias)}")

    criar_index(lista_noticias)

    print("index.html atualizado com sucesso.")
