import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Salão Primus", page_icon="✂️", layout="wide")
st.title("✂️ Salão Primus")

@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    
    creds_dict = {
        "type": "service_account",
        "project_id": "salao-primus",
        "private_key_id": "217b1319e51ce4babbb3904b4a2975e451a1af44",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/WZVaHYSP30d+\nU4BnGmcFTkRo2zXHDNpvm017S9DjZSA/xBkC2oR2LTUNmhg0t8c3DmCPq8LPBp/m\nBjul9EVs2lBB/xQiEqgnv9cCvoCn1a/ZAjgcinpcah53wvhoF0fissK8jBMSx7lm\nfIv9DO+jVuzLxii1nFLGbVN3MJ1K2AJ3vbZiBKHK6Zja7KYeRAiWYP8Jyv/ho6PG\nNUv7EC/BhEo1nO4Wr0ZHoAspJc0fNl/YogBgRHAJWuDK3ConMtb6ONlBB0/pHNdX\nN36sHlgrGLZ5Xe4tH1iQSV2T5MIvKwVi54oJ0wrp4VQMHBvxW0unB7+9KV1ys/8Q\nVvQpbjt1AgMBAAECggEAIS9SV0dMvN3Sao5lM5xQ1wr4kr3HoQ5x2I60vIgMwU8B\nrYVe+A95DvyumX4KqiPgJQR1ix0U4y4JL42PrSuEmcjvx85KydD2ADTFP2jV66WD\nwm0f2ZVLfLj7sTXrOjQlZ6OsYaIiUay5EtTRO1DRw4BY/0sNttdWRKrjoYVZFgg8\niu/IkCBePaYToDE2CdtUTo1+kNy6z5g9pJJ1tyDpt6JzR7tX5A8jIebEz2JQFsHU\n6DZDsbw0hHeIf9ovQIze8rh+g/LtdElh41LVfwpmy+Eb6k8hhxRC4PwVzbdyIQ8J\qxZNPveLQZNBnGSRKplS6ReaY0C4u4zqf2HKWmMFIQKBgQD2NtBeZWQMYRKLPPrG\nXsu++Ea9JjmIqfv5tWSnIq3TAWAiUpA/b7DG1u4jxHFK6rMEkKx3xy4453lj+j6q\n2Osx7Qs4p+hF53lVcCVpemwdTKUkHTJLhyZBP2zv95DT0MtfWaSKepE+dpRCOjln\nrsAcNmbBOr0+uJH9FiYasxS6YQKBgQDG9IkxC5FX+UaaEFMMPI8Po2lRpFZUxt2k\nldl+tG7vHta83daPdYOqYBdraFnoPfaxEVLhR6YJFBs6ZQ9UjOBbMC546CW2xT05\DlSMihOJV1micaJ1L1bXfTYT5DrAw3IKL3w8K7ZPLQg4rPtfPBSD5oeK7/nHOiqF\nSM8vwh9hlQKBgQDOHAjGXL4qFsD9Smjr0sNg9FnTUcJsA1BqM001FLTKpKYjVVZn\npEopyhbEXlgwzNRbh/i4tEafYDagWQZI4xnQS41POlAY5LMPsLfA2rjStiywVLib\nvWFq0XuSTn4wsuLsyRAS1JPt5DosTq1rfEBZ3bibHV76uGuNoBL52twJQQKBgET3\nc686sVFrqduyGPe+7mCfZtzUOND+dsqc314asfHWIN4rkDr+o3ul/7hN3gyxnhhX\RwGs0pOHEsE1UxEeHI+/rfxfjONEkCp9GzX0jz0muH2lIom4tUPRtbNDhFJZ7eg1\+bzp8jKUC6uJ20FyFDJ88TNqaI11TlQRnzCQ/EvZAoGBAJzSqXT/ffeI82VUuEAX\PyuHryG8F/LavqLpl0oUfRePRcIgb4yL8oNjVD3Z6GKXLqoLHggfgQ7btZgS8fqS\nkOUp896CNWr5C25FwIAzZpK9wz+LqM8GmJtsQNOI2Ho16I5JmuPpVGdC9yZMH3T3\nC8gD+YYDU40/rPdExWUo5zqu\n-----END PRIVATE KEY-----",
        "client_email": "robo-salao@salao-primus.iam.gserviceaccount.com",
        "client_id": "108021907186580997029",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/robo-salao%40salao-primus.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1QmaDuA8C0ihw4iQ6CQUDT1vgHEPiKNZtqJQAflbqyC8/edit?usp=sharing")

try:
    sheet = init_connection()
except Exception as e:
    st.error(f"Erro detalhado de conexão: {e}")
    st.stop()
def get_data(worksheet_name, cols):
    try:
        ws = sheet.worksheet(worksheet_name)
    except:
        ws = sheet.add_worksheet(title=worksheet_name, rows=100, cols=20)
        ws.append_row(cols)
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(columns=cols)
    return df, ws

def load_data():
    profissionais, ws_prof = get_data("Profissionais", ['Nome', 'Email', 'Cargo', 'Foto'])
    servicos, ws_serv = get_data("Serviços", ['Nome do Serviço', 'Categoria', 'Valor'])
    comandas, ws_com = get_data("Comandas", ['Nome do Cliente', 'Data', 'Status', 'Total'])
    itens, ws_itens = get_data("Itens da Comanda", ['Nome do Cliente', 'Profissional', 'Serviço', 'Valor'])
    historico, ws_hist = get_data("Histórico", ['Data Fechamento', 'Nome do Cliente', 'Profissional', 'Serviço', 'Valor'])

    if 'Valor' in servicos.columns: servicos['Valor'] = pd.to_numeric(servicos['Valor'], errors='coerce').fillna(0)
    if 'Valor' in itens.columns: itens['Valor'] = pd.to_numeric(itens['Valor'], errors='coerce').fillna(0)
    if 'Valor' in historico.columns: historico['Valor'] = pd.to_numeric(historico['Valor'], errors='coerce').fillna(0)

    return profissionais, servicos, comandas, itens, historico, ws_prof, ws_serv, ws_com, ws_itens, ws_hist

profissionais, servicos, comandas, itens, historico, ws_prof, ws_serv, ws_com, ws_itens, ws_hist = load_data()

def save_df(df, ws):
    ws.clear()
    df = df.fillna("")
    data = [df.columns.values.tolist()] + df.values.tolist()
    ws.update(values=data, range_name='A1')

def get_valor_servico(nome_servico, df_servicos):
    if not df_servicos.empty:
        match_serv = df_servicos[df_servicos['Nome do Serviço'] == nome_servico]
        if not match_serv.empty:
            return float(match_serv['Valor'].values[0])
    return 0.0

menu = st.sidebar.selectbox("Menu", ["Comandas", "Dashboard / Fechamento", "Cadastros"])

if menu == "Comandas":
    st.header("📝 Gerenciar Comandas")
    aba_abertas, aba_nova = st.tabs(["📋 Comandas Abertas", "➕ Abrir Nova Comanda"])
    
    with aba_abertas:
        if itens.empty:
            st.info("Nenhuma comanda aberta no momento. Vá na aba ao lado para abrir uma nova.")
        else:
            clientes_ativos = itens['Nome do Cliente'].unique().tolist()
            st.write("### Clientes em Atendimento")
            cols = st.columns(2) 
            for index, cliente in enumerate(clientes_ativos):
                with cols[index % 2]: 
                    with st.container(border=True):
                        st.subheader(f"👤 {cliente}")
                        itens_cliente = itens[itens['Nome do Cliente'] == cliente]
                        total_cliente = itens_cliente['Valor'].sum()
                        st.markdown(f"**Total da conta:** R$ {total_cliente:.2f}")
                        st.dataframe(itens_cliente[['Profissional', 'Serviço', 'Valor']], use_container_width=True, hide_index=True)
                        
                        with st.form(f"form_add_{cliente}"):
                            prof_add = st.selectbox("Profissional", profissionais['Nome'].tolist() if not profissionais.empty else ["Bruno"], key=f"prof_{cliente}")
                            serv_add = st.selectbox("Serviço", servicos['Nome do Serviço'].tolist() if not servicos.empty else ["Corte"], key=f"serv_{cliente}")
                            submit_add = st.form_submit_button("➕ Adicionar Serviço")
                            
                            if submit_add:
                                val_serv = get_valor_servico(serv_add, servicos)
                                nova_linha = pd.DataFrame({'Nome do Cliente': [cliente], 'Profissional': [prof_add], 'Serviço': [serv_add], 'Valor': [val_serv]})
                                itens = pd.concat([itens, nova_linha], ignore_index=True)
                                save_df(itens, ws_itens)
                                st.success(f"Adicionado para {cliente}!")
                                st.rerun()

    with aba_nova:
        st.subheader("Começar atendimento (Novo Cliente)")
        with st.form("form_nova_comanda"):
            novo_cliente_nome = st.text_input("Nome do Cliente")
            col1, col2 = st.columns(2)
            with col1:
                prof_novo = st.selectbox("Profissional", profissionais['Nome'].tolist() if not profissionais.empty else ["Bruno"])
            with col2:
                serv_novo = st.selectbox("Serviço Inicial", servicos['Nome do Serviço'].tolist() if not servicos.empty else ["Corte"])
            submit_novo = st.form_submit_button("Abrir Comanda")
            
            if submit_novo and novo_cliente_nome:
                val_serv = get_valor_servico(serv_novo, servicos)
                nova_linha = pd.DataFrame({'Nome do Cliente': [novo_cliente_nome.strip()], 'Profissional': [prof_novo], 'Serviço': [serv_novo], 'Valor': [val_serv]})
                itens = pd.concat([itens, nova_linha], ignore_index=True)
                save_df(itens, ws_itens)
                st.success(f"Comanda aberta para {novo_cliente_nome}!")
                st.rerun()

elif menu == "Dashboard / Fechamento":
    st.header("📊 Fechamento da Semana e Comissões")
    if not itens.empty and 'Valor' in itens.columns:
        total_geral = itens['Valor'].sum()
        st.metric(label="Faturamento Bruto da Semana", value=f"R$ {total_geral:.2f}")
        st.divider()
        st.subheader("💰 Cálculo de Pagamento por Profissional")
        faturamento_prof = itens.groupby('Profissional')['Valor'].sum().reset_index()
        
        for index, row in faturamento_prof.iterrows():
            prof_nome = row['Profissional']
            prof_total = row['Valor']
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"### {prof_nome}")
                c1.write(f"Produção total na semana: **R$ {prof_total:.2f}**")
                pct = c2.number_input("Comissão (%)", min_value=0, max_value=100, value=65, step=1, key=f"pct_{prof_nome}")
                valor_receber = prof_total * (pct / 100)
                c3.write("##### Valor a Receber:")
                c3.write(f"### R$ {valor_receber:.2f}")

        st.divider()
        st.subheader("🛑 Fechar a Semana")
        st.warning("Atenção: Clicar no botão abaixo vai zerar as comandas atuais da tela e salvar todas elas no Histórico.")
        if st.button("Encerrar Semana e Salvar Histórico"):
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            itens_salvar = itens.copy()
            itens_salvar['Data Fechamento'] = data_atual
            historico = pd.concat([historico, itens_salvar], ignore_index=True)
            itens = pd.DataFrame(columns=['Nome do Cliente', 'Profissional', 'Serviço', 'Valor'])
            save_df(historico, ws_hist)
            save_df(itens, ws_itens)
            st.success("Semana encerrada com sucesso! Tela zerada para amanhã.")
            st.rerun()
    else:
        st.info("Nenhum atendimento registrado nesta semana ainda.")
        
    st.divider()
    with st.expander("Ver Histórico de Semanas Anteriores"):
        if not historico.empty:
            st.dataframe(historico, use_container_width=True, hide_index=True)
        else:
            st.write("Nenhum histórico salvo ainda.")

elif menu == "Cadastros":
    st.header("⚙️ Cadastros de Equipe e Serviços")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Profissionais")
        st.dataframe(profissionais, use_container_width=True, hide_index=True)
        with st.form("novo_prof"):
            nome_p = st.text_input("Nome do Funcionário")
            cargo_p = st.text_input("Cargo")
            btn_p = st.form_submit_button("Cadastrar Profissional")
            if btn_p and nome_p:
                novo_p = pd.DataFrame({'Nome': [nome_p], 'Email': [''], 'Cargo': [cargo_p], 'Foto': ['']})
                profissionais = pd.concat([profissionais, novo_p], ignore_index=True)
                save_df(profissionais, ws_prof)
                st.success("Profissional adicionado!")
                st.rerun()

    with col2:
        st.subheader("Serviços")
        st.dataframe(servicos, use_container_width=True, hide_index=True)
        with st.form("novo_serv"):
            nome_s = st.text_input("Nome do Serviço")
            cat_s = st.text_input("Categoria")
            val_s = st.number_input("Valor (R$)", min_value=0.0, step=10.0)
            btn_s = st.form_submit_button("Cadastrar Serviço")
            if btn_s and nome_s:
                novo_s = pd.DataFrame({'Nome do Serviço': [nome_s], 'Categoria': [cat_s], 'Valor': [val_s]})
                servicos = pd.concat([servicos, novo_s], ignore_index=True)
                save_df(servicos, ws_serv)
                st.success("Serviço adicionado!")
                st.rerun()
