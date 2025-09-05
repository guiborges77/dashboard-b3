# dashboards/app.py
# =====================================
# Dashboard interativo de Liquidez e Risco - B3 (Top 10)
# =====================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale

# ------------------------
# 0. Configurações gerais
# ------------------------
st.set_page_config(page_title="B3 Liquidez & Risco", layout="wide")
sns.set_theme(style="whitegrid")

# Configurar locale para pt_BR
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Linux/macOS
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Windows

# ------------------------
# 1. Função auxiliar para formatar números
# ------------------------
def format_brl(x, decimals=2, is_currency=True):
    if pd.isna(x):
        return ""
    s = locale.format_string(f"%.{decimals}f", x, grouping=True)
    return f"R$ {s}" if is_currency else s

# ------------------------
# 2. Carregar dados processados
# ------------------------
DATA_FILE = "data/processed/merged_liquidity_risk.csv"

@st.cache_data
def load_data(file_path):
    try:
        # Ler CSV completo
        df = pd.read_csv(file_path, sep=";", dtype=str)

        # Converter colunas numéricas
        num_cols = {
            "NtlFinVol": "TotalVol",
            "AdjstdQt": "TotalQty",
            "MinPric": "MinPrice",
            "MaxPric": "MaxPrice",
            "TradAvrgPric": "AvgPrice"
        }
        for old_col, new_col in num_cols.items():
            if old_col in df.columns:
                df[old_col] = df[old_col].str.replace(",", ".").str.strip()
                df[new_col] = pd.to_numeric(df[old_col], errors='coerce').fillna(0)

        return df

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return pd.DataFrame()

df = load_data(DATA_FILE)

if df.empty:
    st.warning("Arquivo CSV vazio ou não carregado.")
    st.stop()

# ------------------------
# 3. Selecionar top 10 por TotalVol
# ------------------------
df_top = df.nlargest(10, "TotalVol")

# ------------------------
# 4. Sidebar - filtros
# ------------------------
st.sidebar.header("Filtros")
ativos = st.sidebar.multiselect(
    "Selecione ativos:",
    options=df_top["TckrSymb"].unique(),
    default=df_top["TckrSymb"].unique()
)
df_filtered = df_top[df_top["TckrSymb"].isin(ativos)]

# ------------------------
# 5. Métricas resumidas
# ------------------------
st.title("Dashboard de Liquidez e Risco - B3 (Top 10)")
st.subheader("Resumo Geral")

total_qty = df_filtered["TotalQty"].sum()
total_vol = df_filtered["TotalVol"].sum()
min_price = df_filtered["MinPrice"].min()
max_price = df_filtered["MaxPrice"].max()
avg_price = df_filtered["AvgPrice"].mean()

st.metric("Quantidade Total", format_brl(total_qty, 0, is_currency=False))
st.metric("Volume Total", format_brl(total_vol))
st.metric("Preço Mínimo", format_brl(min_price))
st.metric("Preço Máximo", format_brl(max_price))
st.metric("Preço Médio", format_brl(avg_price))

# ------------------------
# 6. Tabelas detalhadas
# ------------------------
st.subheader("Resumo por Ativo (Top 10)")

df_display = df_filtered.copy()

# Formatar colunas para exibição
df_display["Ativo"] = df_display["TckrSymb"]
df_display["Quantidade Total"] = df_display["TotalQty"].apply(lambda x: format_brl(x, 0, is_currency=False))
df_display["Volume Total (R$)"] = df_display["TotalVol"].apply(lambda x: format_brl(x))
df_display["Preço Mínimo (R$)"] = df_display["MinPrice"].apply(lambda x: format_brl(x))
df_display["Preço Máximo (R$)"] = df_display["MaxPrice"].apply(lambda x: format_brl(x))
df_display["Preço Médio (R$)"] = df_display["AvgPrice"].apply(lambda x: format_brl(x))

columns_to_show = ["", "Ativo", "Quantidade Total", "Volume Total (R$)",
                   "Preço Mínimo (R$)", "Preço Máximo (R$)", "Preço Médio (R$)"]

# Criar cópia da primeira coluna sem cabeçalho
df_display[""] = df_display.iloc[:, 0]

st.dataframe(
    df_display[columns_to_show].sort_values(by="Volume Total (R$)", ascending=False)
)

# ------------------------
# 7. Gráficos
# ------------------------
st.subheader("Gráfico de Volume por Ativo")
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=df_filtered, x="TckrSymb", y="TotalVol", palette="viridis", ax=ax)
ax.set_ylabel("Volume Total (R$)")
ax.set_xlabel("Ativo")
ax.set_yticklabels([format_brl(x) for x in ax.get_yticks()])
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Gráfico de Preço Médio por Ativo")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(data=df_filtered, x="TckrSymb", y="AvgPrice", palette="coolwarm", ax=ax2)
ax2.set_ylabel("Preço Médio (R$)")
ax2.set_xlabel("Ativo")
ax2.set_yticklabels([format_brl(x) for x in ax2.get_yticks()])
plt.xticks(rotation=45)
st.pyplot(fig2)

# ------------------------
# 8. Informações adicionais
# ------------------------
st.sidebar.info(
    "Dashboard interativo para análise de liquidez e risco de ativos B3.\n\n"
    "Desenvolvido em Python com Streamlit, Matplotlib e Seaborn."
)
