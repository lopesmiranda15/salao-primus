import streamlit as st

st.set_page_config(page_title="Salão Primus", layout="wide")
st.title("✂️ Salão Primus - Conectado!")

# Conecta na planilha automaticamente usando o Secrets acima
conn = st.connection("gsheets", type="gsheets")

# Lê a primeira aba da planilha para testar
df = conn.read(ttl=0)

st.success("Conectado com sucesso via Streamlit Connection!")
st.write("Dados da planilha:", df)
