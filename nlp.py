import re

def extrair_parametros(texto):
    preco_max = None
    match = re.search(r"até\s*R\$\s*(\d+)", texto)
    if match:
        preco_max = int(match.group(1))

    termo = re.sub(r"até\s*R\$\s*\d+", "", texto).strip()
    return {"termo": termo, "preco_max": preco_max}
