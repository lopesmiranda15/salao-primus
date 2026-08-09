import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Conexão Salão Primus")

creds = Credentials.from_service_account_file(
    "credenciais.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
st.success("CONECTADO COM SUCESSO!")
