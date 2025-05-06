import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Double Analyzer", layout="centered")

st.title("🎲 Double Analyzer - Dados Reais da Blaze")
st.markdown("Análise em tempo real dos últimos resultados da roleta Double da Blaze.")

# Função para obter os resultados reais
def obter_resultados_reais():
    url = "https://blaze.com/api/roulette_games/recent"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        resultados = []

        for jogo in dados:
            cor = jogo['color']  # 0 = vermelho, 1 = preto, 2 = branco
            if cor == 0:
                resultados.append("vermelho")
            elif cor == 1:
                resultados.append("preto")
            elif cor == 2:
                resultados.append("branco")

        return list(reversed(resultados))  # ordem cronológica
    except Exception as e:
        return ["erro"]

# Cores possíveis
num_cores = {'preto': 0, 'vermelho': 1, 'branco': 2}

# Obter dados da API
historico = obter_resultados_reais()

if "erro" in historico:
    st.error("❌ Erro ao acessar a API da Blaze. Tente novamente mais tarde.")
    st.stop()

df = pd.DataFrame({
    'Index': list(range(1, len(historico)+1)),
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
