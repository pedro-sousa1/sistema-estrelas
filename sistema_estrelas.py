import streamlit as st
import json
import os
from datetime import datetime

# Arquivo para salvar os dados
ARQUIVO = "estrelas_streamlit.json"

# Categorias e emojis
CATEGORIAS = ["Estudar", "Malhar", "Alimentação", "Outro"]
EMOJIS = ["🌟", "💫", "✨", "⭐"]

# Criar arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump({"Pedro_para_Isabela": [], "Isabela_para_Pedro": []}, f)

# Carregar dados
with open(ARQUIVO, "r") as f:
    estrelas = json.load(f)

# Função para salvar dados
def salvar():
    with open(ARQUIVO, "w") as f:
        json.dump(estrelas, f, indent=4)

# Contar estrelas do dia
def estrelas_hoje(usuario):
    hoje = datetime.now().strftime("%d/%m/%y")
    return sum(1 for e in estrelas[usuario] if e["dia"] == hoje)

# Login simples
st.title("⭐ Sistema de Estrelas Turbinado ⭐")
usuario_logado = st.radio("Escolha seu usuário", ("Senhor Pedro", "Dona Isabela"))

# Determinar para quem você marca
if usuario_logado == "Senhor Pedro":
    usuario = "Pedro_para_Isabela"
    outro = "Isabela_para_Pedro"
else:
    usuario = "Isabela_para_Pedro"
    outro = "Pedro_para_Isabela"

st.subheader(f"Você está marcando estrelas para { 'Dona Isabela' if usuario_logado=='Senhor Pedro' else 'Senhor Pedro' }")

# Marcar estrela
st.markdown("### Marcar estrela:")
categoria = st.selectbox("Escolha a categoria", CATEGORIAS)
if st.button("Marcar estrela"):
    data = datetime.now().strftime("%d/%m/%y")
    emoji = EMOJIS[CATEGORIAS.index(categoria) % len(EMOJIS)]
    estrelas[usuario].append({"dia": data, "categoria": f"{categoria} {emoji}"})
    salvar()
    st.success(f"⭐ Estrela marcada em {categoria} {emoji}!")

# Mostrar histórico e total
st.markdown("---")
st.subheader("Histórico de estrelas")

st.write(f"**Estrelas do Senhor Pedro** (para {usuario_logado}):")
for e in estrelas["Pedro_para_Isabela"]:
    st.write(f"{e['dia']} - {e['categoria']}")
st.write(f"Total: {len(estrelas['Pedro_para_Isabela'])} | Hoje: {estrelas_hoje('Pedro_para_Isabela')}")

st.write(f"**Estrelas da Dona Isabela** (para {usuario_logado}):")
for e in estrelas["Isabela_para_Pedro"]:
    st.write(f"{e['dia']} - {e['categoria']}")
st.write(f"Total: {len(estrelas['Isabela_para_Pedro'])} | Hoje: {estrelas_hoje('Isabela_para_Pedro')}")
