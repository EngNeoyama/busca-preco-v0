import streamlit as st
from busca import buscar_produtos
from nlp import extrair_parametros

st.set_page_config(page_title="Busca de Preços", layout="centered")
st.title("🔍 Bot de Busca de Preços")

consulta = st.text_input("Digite o que você procura (ex: 'multímetro até R$150'):")

if st.button("Pesquisar"):
    if consulta:
        st.info("Buscando...")
        parametros = extrair_parametros(consulta)
        resultados = buscar_produtos(parametros)

        if resultados:
            for r in resultados:
                st.markdown(f"**{r['nome']}**\n\n💰 R${r['preco']}\n\n🔗 [Ver produto]({r['link']})\n---")
        else:
            st.warning("Nenhum resultado encontrado.")
    else:
        st.warning("Digite uma consulta válida.")
