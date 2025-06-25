import datetime as dt
import streamlit as st
import pandas as pd
from data import load_colaboradores, save_colaboradores, append_pedido

st.set_page_config(page_title="Pedido de Uniforme", page_icon="🧢")

st.title("Pedido de Uniforme 👕👖")

# ---------- Login simples --------------
mat = st.text_input("Matrícula")
if not mat:
    st.stop()

df_colab = load_colaboradores()
linhas = df_colab[df_colab["Matricula"] == mat]

if linhas.empty:
    st.info("Matrícula não encontrada. Cadastre-se:")
    nome   = st.text_input("Nome completo")
    funcao = st.text_input("Função")
    setor  = st.text_input("Setor")
    genero = st.selectbox("Gênero", ("M", "F"))
    if st.button("Salvar cadastro"):
        novo = {
            "Matricula": mat, "Nome": nome, "Funcao": funcao,
            "Setor": setor, "Genero": genero, "UltimoPeriodico": ""
        }
        df_colab = df_colab.append(novo, ignore_index=True)
        save_colaboradores(df_colab)
        st.success("Cadastro salvo! Atualize a página.")
    st.stop()

# ---------- Formulário de pedido -------
colab = linhas.iloc[0]
st.success(f"Bem-vindo(a), {colab['Nome']}")

tipo = st.radio("Tipo de pedido", ("Periódico", "Troca"), horizontal=True)

KIT_MASC = ["2 Camisas", "2 Calças", "2 Gravatas", "1 Jaqueta"]
KIT_FEM  = ["2 Spencers", "1 Tricot de lã", "2 Calças", "1 Saia",
            "1 Blazer", "2 Encharpes", "1 Prendedor de lenço"]

if tipo == "Periódico":
    itens = KIT_MASC if colab["Genero"] == "M" else KIT_FEM
    st.write("Kit:", ", ".join(itens))
    itens_sel = itens
    justificativa = ""
else:
    ALL = ["Camisa", "Calça", "Gravata", "Jaqueta",
           "Spencer", "Tricot de lã", "Saia", "Blazer",
           "Encharpe", "Prendedor de lenço"]
    itens_sel = st.multiselect("Selecione itens", ALL)
    justificativa = st.text_area("Justificativa")

if st.button("Enviar pedido"):
    if not itens_sel:
        st.warning("Selecione pelo menos um item.")
        st.stop()
    row = {
        "Timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Matricula": mat,
        "Nome": colab["Nome"],
        "TipoPedido": tipo,
        "Itens": "; ".join(itens_sel),
        "Justificativa": justificativa,
        "Status": "Pendente"
    }
    append_pedido(row)
    st.success("Pedido enviado! 👍")
