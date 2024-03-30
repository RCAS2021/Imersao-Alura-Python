import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Baixando tabela do yahoo finances das ações da petrobras
df_dados = yf.download("PETR4.SA", start="2023-01-01", end="2023-12-31")

# Renomeando as colunas
df_dados.columns = ["Abertura", "Maximo", "Minimo", "Fechamento", "Fech_ajust", "Volume"]

# Renomeando índice
df_dados = df_dados.rename_axis("Data")

# Plotando gráfico com valores de fechamento
df_dados["Fechamento"].plot(figsize=(10,6))
# Adicionando título ao gráfico
plt.title("Variação preço por data", fontsize=16)
# Adicionando legenda ao gráfico
plt.legend(["Fechamento"])
# Mostrando o gráfico
#plt.show()

# Pegando as 60 primeiras linhas
df = df_dados.head(60).copy()

# Transformando a coluna data no índice
df["Data"] = df.index

# Transformando os valores da coluna data de data pra número
df["Data"] = df["Data"].apply(mdates.date2num)

# Plotando gráfico de candlestick
# Gerando figure e axis
fig, ax = plt.subplots(figsize=(15, 8))

# Configurando largura
width = 0.7

# Estrutura loop para popular a figura
for i in range(len(df)):
    # Condicional para checar se o valor subiu(verde) ou desceu(vermelho)
    if df["Fechamento"].iloc[i] > df["Abertura"].iloc[i]:
        color = "green"
    else:
        color = "red"

    # Plotagem dos dados no eixo, x = Datas, y = Mínimo e Máximo, cor = cor(verde ou vermelho), largura da linha = 1
    ax.plot([df["Data"].iloc[i], df["Data"].iloc[i]],
        [df["Minimo"].iloc[i], df["Maximo"].iloc[i]],
        color = color,
        linewidth = 1)
    
    # Adicionando os retângulos do gráfico, adicionando patch e plotando um retângulo, Centralizando o retângulo, encontrando o mínimo entre fechamento e abertura, configurando o xy
    # Configurando a largura para ser igual a largura previamente configurada
    # Calculando o módulo entre fechamento e abertura, configurando a altura
    # Configurando a cor = cor(verde ou vermelho)
    ax.add_patch(plt.Rectangle((df["Data"].iloc[i] - width/2, min(df["Abertura"].iloc[i], df["Fechamento"].iloc[i])),
                            width,
                            abs(df["Fechamento"].iloc[i] - df["Abertura"].iloc[i]),
                            facecolor=color))

# Gerando as médias móveis 7 dias
df["MA7"] = df["Fechamento"].rolling(window=7).mean()
# Gerando as médias móveis 14 dias
df["MA14"] = df["Fechamento"].rolling(window=14).mean()

# Plotando linha no gráfico com a média móvel de 7 dias
ax.plot(df["Data"], df["MA7"], color="orange", label="Média móvel 7 dias")
# Plotando linha no gráfico com a média móvel de 14 dias
ax.plot(df["Data"], df["MA14"], color="yellow", label="Média móvel 14 dias")
# Adicionando legenda
ax.legend()

# Configurando o axis x para datas
ax.xaxis_date()
# Formatando o valor das datas
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
# Rotacionando o axis x em 45 graus
plt.xticks(rotation=45)

# Adicionando título
plt.title("Gráfico de Candlestick - PETR4.SA com matplotlib")
# Adicionando label axis x
plt.xlabel("Data")
# Adicionando label axis y
plt.ylabel("Preço")

# Adicionando grid para melhor visualização
plt.grid(True)

# Mostrando o gráfico
#plt.show()

# Adicionando interatividade

# Gerando 2 subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("Candlesticks", "Volume Transacionado"), row_width=[0.2, 0.7])
# Adicionando gráfico candlestick, passando os valores como parâmetros e adicionando o gráfico à linha 1
fig.add_trace(go.Candlestick(x=df.index, open=df["Abertura"], high=df["Maximo"], low=df["Minimo"], close=df["Fechamento"], name="Candlestick"), row=1, col=1)
# Adicionando os gráficos de linha para as médias móveis ao gráfico na linha 1
fig.add_trace(go.Scatter(x=df.index, y=df["MA7"], mode="lines", name="MA7 - Média móvel 7 dias"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["MA14"], mode="lines", name="MA14 - Média móvel 14 dias"), row=1, col=1)

# Adicionando gráfico de barras na linha 2
fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), row=2, col=1)

# Atualizando o layout, adicionando o title do eixo y e suas dimensões
fig.update_layout(yaxis_title="Preço", xaxis_rangeslider_visible=False, width=1100, height=600)

# Mostrando o gráfico
#fig.show()

# Gerando gráfico em uma linha, sem interatividade
# Rebaixando a tabela inicial
df_dados = yf.download("PETR4.SA", start="2023-01-01", end="2023-12-31")

# Utilizando o mplfinance para plotar o gráfico de candlestick
mpf.plot(df_dados.head(30), type="candle", figsize=(16,8), volume=True, mav=(7,14), style="yahoo")
#plt.show()

# Outro exemplo
# Baixando os dados das ações da Apple
df_dados_apple = yf.download("AAPL", start="2023-01-01", end="2023-12-31")

# Utilizando o mplfinance para plotar o gráfico de candlestick com os valores da apple
mpf.plot(df_dados_apple, type="candle", figsize=(16,8), volume=True, mav=(7,14), style="yahoo")
#plt.show()