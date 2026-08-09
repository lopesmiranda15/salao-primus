import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

# Configuração da página
st.set_page_config(page_title="Salão Primus", layout="wide")

@st.cache_resource
def init_connection():
    # 1. Pega o JSON das variáveis de ambiente do Streamlit (nuvem)
    creds_json = st.secrets["GCP_CREDENTIALS"]
    creds_dict = json.loads(creds_json)
    
    # 2. Conecta
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    
    # 3. Abre a planilha (use o ID da sua planilha)
    return client.open_by_key("1QmaDuA8C0ihw4iQ6CQUDT1vgHEPiKNZtqJQAflbqyC8")

# Conexão
try:
    sheet = init_connection()
    st.success("Conectado na nuvem!")
except Exception as e:
    st.error(f"Erro ao conectar: {e}")
    st.stop()

# ... (restante do seu código de tabelas e botões aqui)
