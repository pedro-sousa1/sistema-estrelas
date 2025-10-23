import streamlit as st
import json
import os
from datetime import datetime

# Nome do arquivo
ARQUIVO = "daily_star.json"

# Categorias e emojis
CATEGORIAS = ["Estudar", "Treinar", "Alimentação", "Momento Devocional", "Outro"]
EMOJIS = ["🌟", "💫", "✨", "⭐"]

# Cria arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump({"Pedro_para_Isabela": {}, "Isabela_para_Pedro": {}}, f)

# Carrega dados
with open(ARQUIVO, "r") as f:
    estrelas = json.load(f)

# Função para salvar
def salvar():
    with open(ARQUIVO, "w") as f:
        json.dump(estrelas, f, indent=4)

# Função para contar estrelas do dia
def estrelas_hoje(usuario):
    hoje = datetime.now().strftime("%d/%m/%y")
    if hoje in estrelas[usuario]:
        return len(estrelas[usuario][hoje])
    return 0

# ---------------- INTERFACE STREAMLIT ----------------

st.title("🌠 DAILY-STAR 🌠")
st.markdown("### ⭐ daily star ")

# Login simples
usuario_logado = st.radio("Quem está usando o sistema?", ["Senhor Pedro", "Dona Isabela"])

if usuario_logado == "Senhor Pedro":
    usuario = "Pedro_para_Isabela"
    destino = "Isabela"
else:
    usuario = "Isabela_para_Pedro"
    destino = "Pedro"

st.subheader(f"Você está marcando estrelas para {destino} 💖")

# Escolher categoria
categoria = st.selectbox("Escolha a categoria:", CATEGORIAS)

# Botão para marcar estrela
if st.button("Marcar Estrela ⭐"):
    data = datetime.now().strftime("%d/%m/%y")
    emoji = EMOJIS[CATEGORIAS.index(categoria) % len(EMOJIS)]

    if data not in estrelas[usuario]:
        estrelas[usuario][data] = []
    estrelas[usuario][data].append(f"{categoria} {emoji}")

    salvar()
    st.success(f"Estrela marcada com sucesso em {categoria} {emoji}!")

# ---------------- REMOVER ESTRELA ----------------
st.markdown("---")
st.subheader("❌ Remover Estrela Marcada")

# Mostrar apenas se houver estrelas
if estrelas[usuario]:
    datas_disponiveis = list(estrelas[usuario].keys())
    data_escolhida = st.selectbox("Escolha o dia:", datas_disponiveis)

    if data_escolhida:
        estrelas_dia = estrelas[usuario][data_escolhida]
        estrela_escolhida = st.selectbox("Escolha a estrela para apagar:", estrelas_dia)

        if st.button("Apagar Estrela 🗑️"):
            estrelas[usuario][data_escolhida].remove(estrela_escolhida)

            # Se o dia ficar vazio, remove o dia do dicionário
            if not estrelas[usuario][data_escolhida]:
                del estrelas[usuario][data_escolhida]

            salvar()
            st.success(f"Estrela '{estrela_escolhida}' removida com sucesso!")
else:
    st.info("Nenhuma estrela registrada ainda para remover.")

# ---------------- HISTÓRICO ----------------
st.markdown("---")
st.subheader("📜 Histórico de Estrelas")

# Função auxiliar pra exibir
def exibir_estrelas(usuario, titulo):
    st.write(f"### {titulo}")
    if estrelas[usuario]:
        for dia, atividades in estrelas[usuario].items():
            st.write(f"📅 **{dia}**")
            for a in atividades:
                st.write(f"- {a}")
    else:
        st.write("_Nenhuma estrela registrada ainda._")

    total = sum(len(v) for v in estrelas[usuario].values())
    st.write(f"**Total:** {total} estrelas | **Hoje:** {estrelas_hoje(usuario)}")
    st.markdown("---")

# Mostrar histórico de ambos
exibir_estrelas("Pedro_para_Isabela", "⭐ Estrelas que Pedro deu para Isabela")
exibir_estrelas("Isabela_para_Pedro", "⭐ Estrelas que Isabela deu para Pedro")

