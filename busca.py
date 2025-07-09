import requests
import re

SERPAPI_KEY = "SUA_CHAVE_SERPAPI"  # Substitua pela sua chave do SerpApi

REGEX_PRECO = r"R\$ ?\d{1,3}(?:\.\d{3})*,\d{2}"

def buscar_links_serpapi(termo, max_resultados=6):
    url = "https://serpapi.com/search"
    params = {
        "q": termo,
        "engine": "google",
        "api_key": SERPAPI_KEY,
        "num": max_resultados,
        "hl": "pt-br",
        "gl": "br"
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    links = []
    if "organic_results" in data:
        for item in data["organic_results"]:
            if "link" in item:
                links.append(item["link"])
    return links

def extrair_precos_html(html):
    precos = re.findall(REGEX_PRECO, html)
    precos_float = []
    for preco in precos:
        valor = preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            precos_float.append(float(valor))
        except Exception:
            continue
    return precos_float

def buscar_preco_medio(parametros):
    termo = parametros["termo"]
    preco_max = parametros.get("preco_max")
    links = buscar_links_serpapi(termo)
    todos_precos = []
    for link in links:
        try:
            r = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if r.status_code == 200:
                html = r.text
                precos = extrair_precos_html(html)
                if preco_max:
                    precos = [p for p in precos if p <= preco_max]
                todos_precos += precos
        except Exception as e:
            print(f"Erro ao acessar {link}: {e}")
            continue
    if todos_precos:
        media = sum(todos_precos) / len(todos_precos)
        return round(media, 2)
    return None
