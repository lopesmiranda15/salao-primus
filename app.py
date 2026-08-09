import streamlit as st
import gspread
import os
from google.oauth2.service_account import Credentials

st.title("Conexão")

# LISTA O QUE ELE ENCONTRA NA PASTA PARA VOCÊ VER
st.write("Arquivos na pasta:", os.listdir('.'))

if os.path.exists("credenciais.json"):
    creds = Credentials.from_service_account_file(
        "credenciais.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    st.success("CONECTADO!")
else:
    st.error("ARQUIVO NAO ENCONTRADO")
