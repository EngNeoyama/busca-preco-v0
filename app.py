import streamlit as st
from busca import buscar_preco_medio
from nlp import extrair_parametros

st.set_page_config(page_title="Busca de Preços", layout="centered")
st.title("🔍 Bot de Preço Médio")

consulta = st.text_input("Digite o que você procura (ex: 'multímetro até R$150'):")

if st.button("Pesquisar"):
    if consulta:
        st.info("Buscando...")
        parametros = extrair_parametros(consulta)
        media = buscar_preco_medio(parametros)

        if media:
            st.success(f"💰 Preço médio estimado: **R$ {media:.2f}**")
        else:
            st.warning("Nenhum resultado encontrado.")
    else:
        st.warning("Digite uma consulta válida.")
