import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Double Analyzer", layout="centered")
st.title("🎲 Double Analyzer - Dados Reais (via API pública)")
st.markdown("Análise em tempo real da roleta Double da Blaze via API de terceiros.")

# Nova função para acessar API alternativa
def obter_resultados_alternativo():
    url = "https://blaze-api-roulettes.vercel.app/api/double"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        resultados = [jogada['color'] for jogada in data['records']]
        return resultados[:50]  # pegar os últimos 50
    except Exception as e:
        return ["erro"]

# Cores possíveis
num_cores = {'preto': 0, 'vermelho': 1, 'branco': 2}

# Obter dados reais
historico = obter_resultados_alternativo()

if "erro" in historico:
    st.error("❌ Erro ao acessar a API pública de terceiros.")
    st.stop()

# DataFrame para exibição e análise
df = pd.DataFrame({
    'Index': list(range(1, len(historico) + 1)),
    'Cor': historico,
    'Valor': [num_cores[c] for c in historico]
})

st.subheader("📊 Últimas jogadas (Blaze)")
st.dataframe(df[['Index', 'Cor']].set_index('Index'))

# Gráfico
st.subheader("📈 Gráfico de sequência")
fig, ax = plt.subplots()
ax.plot(df['Index'], df['Valor'], marker='o', linestyle='-')
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['Preto', 'Vermelho', 'Branco'])
ax.set_xlabel("Jogada")
ax.set_ylabel("Cor")
ax.grid(True)
st.pyplot(fig)

# Análise simples
ultimas = historico[-5:]
st.subheader("🧠 Análise dos últimos 5 resultados:")
st.write("Últimas jogadas:", ultimas)

if ultimas.count('vermelho') >= 4:
    st.warning("⚠️ Tendência de VERMELHO! Possível inversão para PRETO.")
elif ultimas.count('preto') >= 4:
    st.warning("⚠️ Tendência de PRETO! Possível inversão para VERMELHO.")
elif 'branco' in ultimas:
    st.info("⚪ Saiu BRANCO recentemente. Padrões podem mudar.")
else:
    st.success("🔄 Sem padrão dominante detectado.")
