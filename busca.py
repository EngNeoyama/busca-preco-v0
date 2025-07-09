import requests
import re
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# Regex para encontrar preços em formato brasileiro
REGEX_PRECO = r"R\$ ?\d{1,3}(?:\.\d{3})*,\d{2}"

def buscar_links_duckduckgo(termo, max_resultados=6):
    links = []
    with DDGS() as ddgs:
        for r in ddgs.text(termo, max_results=max_resultados):
            # Preferir sites conhecidos de e-commerce, mas pode pegar qualquer um
            links.append(r['href'])
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
    links = buscar_links_duckduckgo(termo)
    print("Links encontrados:", links)  # LOG
    todos_precos = []
    for link in links:
        try:
            print(f"Buscando preços em: {link}")  # LOG
            r = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if r.status_code == 200:
                html = r.text
                precos = extrair_precos_html(html)
                print(f"Preços encontrados em {link}: {precos}")  # LOG
                if preco_max:
                    precos = [p for p in precos if p <= preco_max]
                todos_precos += precos
            else:
                print(f"Falha ao acessar {link}: {r.status_code}")  # LOG
        except Exception as e:
            print(f"Erro ao acessar {link}: {e}")
            continue
    print("Todos os preços encontrados:", todos_precos)
    if todos_precos:
        media = sum(todos_precos) / len(todos_precos)
        return round(media, 2)
    return None
