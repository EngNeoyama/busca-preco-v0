import re

def extrair_parametros(texto):
    preco_max = None
    match = re.search(r"até\s*R\$\s*(\d+)", texto)
    if match:
        preco_max = int(match.group(1))

    # Remoção de vírgulas e termos desnecessários
    termo_limpo = re.sub(r"[,:]", "", texto)
    termo_limpo = re.sub(r"(?i)(marca|pot[êe]ncia|alimenta[çc][ãa]o|até R\$ \d+)", "", termo_limpo).strip()

    return {"termo": termo_limpo, "preco_max": preco_max}
