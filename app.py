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
        resultado = buscar_preco_medio(parametros)

        if resultado["media"]:
            st.success(f"💰 Preço médio estimado: **R$ {resultado['media']:.2f}**")
            st.markdown(
                f"**Extrato da busca:**\n"
                f"- Sites com preços utilizados: **{resultado['num_sites']}**\n"
                f"- Preços analisados: **{resultado['num_precos']}**"
            )
        else:
            st.warning("Nenhum resultado encontrado.")
    else:
        st.warning("Digite uma consulta válida.")
