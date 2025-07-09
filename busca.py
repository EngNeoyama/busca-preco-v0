import requests
from bs4 import BeautifulSoup

def buscar_produtos(parametros):
    termo = parametros["termo"].replace(" ", "-")
    preco_max = parametros["preco_max"]
    url = f"https://lista.mercadolivre.com.br/{termo}"

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    resultados = []
    for item in soup.select(".ui-search-result__content"):
        try:
            nome = item.select_one("h2").text.strip()
            preco_text = item.select_one(".price-tag-fraction").text.replace(".", "")
            preco = int(preco_text)
            link = item.find("a")["href"]
            if not preco_max or preco <= preco_max:
                resultados.append({"nome": nome, "preco": preco, "link": link})
        except:
            continue

    return resultados[:5]
