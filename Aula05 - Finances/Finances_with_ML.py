import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

# Baixando os dados da JNJ
dados = yf.download("JNJ", start="2020-01-01", end="2023-12-31", progress=False)
dados = dados.reset_index()

# Alocando períodos para treino / teste
dados_treino = dados[dados["Date"] < "2023-07-31"]
dados_teste = dados[dados["Date"] >= "2023-07-31"]

# Renomeando colunas para atender aos requisitos de nome
dados_prophet_treino = dados_treino[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

# Utilizando o modelo Prophet com seus parametros
modelo = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False)

# Adicionando feriados ao modelo
modelo.add_country_holidays(country_name="US")

# Realizando o fit do modelo
modelo.fit(dados_prophet_treino)

# Gerando dataframe futuro
futuro = modelo.make_future_dataframe(periods=150)
# Realizando a previsão do dataframe
previsao = modelo.predict(futuro)

# Plotando gráfico
# Configurando dimensões da figure
plt.figure(figsize=(14, 8))
# Plotando dados de treino
plt.plot(dados_treino["Date"], dados_treino["Close"], label="Dados de Treino", color="blue")
# Plotando dados de teste
plt.plot(dados_teste["Date"], dados_teste["Close"], label="Dados Reais (Teste)", color="green")
# Plotando dados da previsão
plt.plot(previsao["ds"], previsao["yhat"], label="Previsão", color="orange", linestyle="--")

# Plotando linha tracejada vertical para indicar o início da previsão
plt.axvline(dados_treino["Date"].max(), color="red", linestyle="--", label="Início da Previsão")
# Adicionando label ao eixo x
plt.xlabel("Data")
# Adicionando label ao eixo y
plt.ylabel("Preço de Fechamento")
# Adicionando título
plt.title("Previsão de Preço de Fechamento vs Dados Reais")
# Adicionando legendas
plt.legend()
# Mostrando o gráfico
#plt.show()

# Realizando mesmos passos, agora para ações da Petrobras
dados2 = yf.download("PETR4.SA", start="2020-01-01", end="2024-02-29")
dados2 = dados2.reset_index()

dados2_treino = dados2[dados2["Date"] < "2023-12-31"]
dados2_teste = dados2[dados2["Date"] >= "2023-12-31"]

dados2_prophet_treino = dados2_treino[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

modelo = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=True)

modelo.add_country_holidays(country_name="BR")

modelo.fit(dados2_prophet_treino)

futuro = modelo.make_future_dataframe(periods=120)
previsao = modelo.predict(futuro)

plt.figure(figsize=(14, 8))
plt.plot(dados2_treino["Date"], dados2_treino["Close"], label="Dados de Treino", color="blue")
plt.plot(dados2_teste["Date"], dados2_teste["Close"], label="Dados Reais (Teste)", color="green")
plt.plot(previsao["ds"], previsao["yhat"], label="Previsão", color="orange", linestyle="solid")

plt.axvline(dados2_treino["Date"].max(), color="red", linestyle="--", label="Início da Previsão")
plt.xlabel("Data")
plt.ylabel("Preço de Fechamento")
plt.title("Previsão de Preço de Fechamento vs Dados Reais")
plt.legend()
plt.show()