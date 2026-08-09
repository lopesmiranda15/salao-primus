import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Salão Primus", page_icon="✂️", layout="wide")
st.title("✂️ Conexão Salão Primus")

@st.cache_resource
def init_connection():
    # Pega o conteúdo que você salvou no Secrets
    creds_json = st.secrets["GCP_CREDENTIALS"]
    
    # Converte o texto JSON em um dicionário que o Google entende
    creds_dict = json.loads(creds_json)
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    
    # Abre a planilha pelo ID
    return client.open_by_key("1QmaDuA8C0ihw4iQ6CQUDT1vgHEPiKNZtqJQAflbqyC8")

# Botão de teste para ver se a conexão funciona
if st.button("Testar Conexão"):
    try:
        sheet = init_connection()
        st.success("Tudo certo! Conexão estabelecida com sucesso.")
        # Se conectou, tenta ler uma aba só para garantir
        ws = sheet.get_worksheet(0)
        st.write("Planilha conectada:", ws.title)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
