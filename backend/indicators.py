import pandas as pd

# Рассчитываем SMA (простая скользящая средняя)
def calculate_sma(data: pd.Series, period: int):
    return data.rolling(window=period, min_periods=1).mean()

# Рассчитываем EMA (экспоненциальная скользящая средняя)
def calculate_ema(data: pd.Series, period: int):
    return data.ewm(span=period, adjust=False).mean()
