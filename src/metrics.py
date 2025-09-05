import pandas as pd
import numpy as np # Necessário para o cálculo da volatilidade

def calc_volatility(df_daily: pd.DataFrame, ticker: str) -> float:
    """Calcula a volatilidade anualizada de um ativo."""
    # Filtra o DataFrame para o ticker específico e ordena por data
    df_ticker = df_daily[df_daily["ticker"] == ticker].sort_values("date")
    
    if df_ticker.empty:
        return 0.0 # Retorna 0 se o ticker não for encontrado

    # Calcula os retornos percentuais diários
    returns = df_ticker["close_price"].pct_change().dropna()
    
    if returns.empty:
        return 0.0 # Retorna 0 se não houver retornos suficientes

    # Calcula o desvio padrão dos retornos e anualiza (252 dias de pregão)
    return returns.std() * np.sqrt(252)

def calc_drawdown(df_daily: pd.DataFrame, ticker: str) -> float:
    """Calcula o drawdown máximo de um ativo."""
    # Filtra o DataFrame para o ticker específico e ordena por data
    df_ticker = df_daily[df_daily["ticker"] == ticker].sort_values("date")
    
    if df_ticker.empty:
        return 0.0 # Retorna 0 se o ticker não for encontrado

    prices = df_ticker["close_price"]
    
    # Calcula o máximo acumulado
    cum_max = prices.cummax()
    
    # Calcula o drawdown
    drawdown = (prices - cum_max) / cum_max
    
    # Retorna o drawdown máximo (o valor mínimo, que é o mais negativo)
    return drawdown.min() if not drawdown.empty else 0.0
