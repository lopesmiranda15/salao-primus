import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Salão Primus", layout="wide")
st.title("✂️ Conexão Salão Primus")

@st.cache_resource
def init_connection():
    # Isso lê o arquivo que você subiu no GitHub, ignorando o painel de Secrets
    return Credentials.from_service_account_file(
        "credenciais.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

try:
    creds = init_connection()
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1QmaDuA8C0ihw4iQ6CQUDT1vgHEPiKNZtqJQAflbqyC8")
    st.success("Conectado com sucesso!")
    st.write("Planilha encontrada:", sheet.title)
except Exception as e:
    st.error(f"Erro ao ler arquivo ou conectar: {e}")
