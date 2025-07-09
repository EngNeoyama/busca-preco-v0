import requests
from bs4 import BeautifulSoup

def buscar_preco_medio(parametros):
    termo = parametros["termo"].lower().replace(" ", "-")
    preco_max = parametros["preco_max"]
    url = f"https://lista.mercadolivre.com.br/{termo}"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return None

    precos = []
    for item in soup.select(".ui-search-result__content"):
        try:
            preco_text = item.select_one(".price-tag-fraction").text.replace(".", "")
            preco = int(preco_text)
            if not preco_max or preco <= preco_max:
                precos.append(preco)
        except:
            continue

    if precos:
        media = sum(precos) / len(precos)
        return round(media, 2)
    else:
        return None
