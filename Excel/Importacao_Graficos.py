import pandas as pd
import plotly.express as px

# Alterando a formatação de números float
pd.options.display.float_format = "{:,.2f}".format

# Importando as páginas
df_principal = pd.read_excel("Imersão Python - Tabela de ações.xlsx", sheet_name="Principal")

df_total_acoes = pd.read_excel("Imersão Python - Tabela de ações.xlsx", sheet_name="Total_de_acoes")

df_ticker = pd.read_excel("Imersão Python - Tabela de ações.xlsx", sheet_name="Ticker")

df_chat_gpt = pd.read_excel("Imersão Python - Tabela de ações.xlsx", sheet_name="ChatGPT")

# Copiando apenas as colunas que serão utilizadas
df_principal = df_principal[["Ativo", "Data", "Último (R$)", "Var. Dia (%)"]].copy()

# Renomeando as colunas
df_principal = df_principal.rename(columns={"Último (R$)": "valor_final", "Var. Dia (%)": "variacao_diaria_pct"}).copy()

# Calculando a variação diária em porcento
df_principal["var_pct"] = df_principal["variacao_diaria_pct"] / 100

# Calculando o valor inicial
df_principal["valor_inicial"] = df_principal["valor_final"] / (df_principal["var_pct"] + 1)

# Calculando variação, resultado
# Juntando à esquerda, df_principal(Ativo) e df_total_acoes(Código)
df_principal = df_principal.merge(df_total_acoes, left_on="Ativo", right_on="Código", how="left")

# Removendo coluna código
df_principal = df_principal.drop(columns="Código")

# Renomeando colunas
df_principal = df_principal.rename(columns={"Qtde. Teórica": "quantidade_teorica"})

# Calculando a variação em reais
df_principal["variacao_rs"] = (df_principal["valor_final"] - df_principal["valor_inicial"]) * df_principal["quantidade_teorica"]

# Transformando tipo da coluna em inteiro
df_principal["quantidade_teorica"] = df_principal["quantidade_teorica"].astype(int)

# Calculando se o valor subiu, desceu ou se manteve estável
df_principal["resultado"] = df_principal["variacao_rs"].apply(lambda x: "Subiu" if x > 0 else ("Desceu" if x < 0 else "Estavel"))

# Pegando nomes das empresas
# Juntando à esquerda, df_principal(Ativo), df_ticker(Ticker)
df_principal = df_principal.merge(df_ticker, left_on="Ativo", right_on="Ticker", how="left")

# Removendo coluna Ticker
df_principal = df_principal.drop(columns=["Ticker"])

# Calculando categoria de idade
# Juntando à esquerda, df_principal(Nome), df_chat_gpt(Empresa)
df_principal = df_principal.merge(df_chat_gpt, left_on="Nome", right_on="Empresa", how="left")

# Removendo coluna Empresa
df_principal = df_principal.drop(columns=["Empresa"])

# Calculando categoria de idade das empresas
df_principal["cat_idade"] = df_principal["Idade (anos)"].apply(lambda x: "Mais de 100 anos" if x > 100 else ("Menos de 50 anos" if x < 50 else "Entre 50 - 100 anos"))

# Removendo duplicatas
df_principal = df_principal.drop_duplicates("Ativo")

# Calculando max, min, media, media_positiva e media_negativa
maior = df_principal["variacao_rs"].max()
print(f"{maior:,.2f}")
menor = df_principal["variacao_rs"].min()
print(f"{menor:,.2f}")
media = df_principal["variacao_rs"].mean()
print(f"{media:,.2f}")
media_subiu = df_principal[df_principal["resultado"] == "Subiu"]["variacao_rs"].mean()
print(f"{media_subiu:,.2f}")
media_desceu = df_principal[df_principal["resultado"] == "Desceu"]["variacao_rs"].mean()
print(f"{media_desceu:,.2f}")

# Criando novo dataframe com linhas onde resultado = subiu
df_principal_subiu = df_principal[df_principal["resultado"] == "Subiu"]
# Criando novo dataframe com linhas onde resultado = desceu
df_principal_desceu = df_principal[df_principal["resultado"] == "Desceu"]

# Calculando a soma da variação positiva em reais, por segmento
df_analise_segmento_subiu = df_principal_subiu.groupby("Segmento")["variacao_rs"].sum().reset_index()
print(df_analise_segmento_subiu)

# Calculando a soma da variação negativa em reais, por segmento
df_analise_segmento_desceu = df_principal_desceu.groupby("Segmento")["variacao_rs"].sum().reset_index()
print(df_analise_segmento_desceu)

# Calculando a soma da variação total em reais, por segmento
df_analise_segmento_total = df_principal.groupby("Segmento")["variacao_rs"].sum().reset_index()
print(df_analise_segmento_total)

# Calculando a soma da variação total em reais, por resultado
df_analise_saldo = df_principal.groupby("resultado")["variacao_rs"].sum().reset_index()
print(df_analise_saldo)

# Formatando texto para utilizar no gráfico
text = [f"{val:,.2f}" for val in df_analise_saldo["variacao_rs"]]

# Gerando gráfico de barras
fig = px.bar(df_analise_saldo, x="resultado", y="variacao_rs", text=text, title="Variação Reais por Resultado")
# Mostrando o gráfico
#fig.show()

# Gerando gráfico de pizza
fig = px.pie(df_analise_segmento_subiu, names="Segmento", values="variacao_rs", title="Variação Reais por Segmento")
# Mostrando o gráfico
#fig.show()

# Calculando soma da variação em reais, por categoria de idade
df_analise_idade = df_principal.groupby("cat_idade")["variacao_rs"].sum().reset_index()
print(df_analise_idade)

# Formatando texto para utilizar no gráfico
text = [f"{val:,.2f}" for val in df_analise_idade["variacao_rs"]]

# Gerando gráfico de barras
fig = px.bar(df_analise_idade, x="cat_idade", y="variacao_rs", text=text, title="Variação Reais por Categoria de idade")
# Mostrando o gráfico
#fig.show()