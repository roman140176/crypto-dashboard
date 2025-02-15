import requests
import pandas as pd
import os
import json

CACHE_FILE = "data/cache.json"


# Функция для конвертации ключей (Timestamp → str)
def convert_keys_to_str(data):
    if isinstance(data, dict):
        return {str(k): convert_keys_to_str(v) for k, v in data.items()}
    if isinstance(data, pd.Timestamp):
        return str(data)
    return data


# Функция загрузки кеша
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Ошибка JSONDecodeError: очищаем кеш!")
                return {}  # Если файл битый, создаём новый кэш
    return {}


# Функция сохранения кеша
def save_cache(cache):
    with open(CACHE_FILE, "w") as file:
        json.dump(convert_keys_to_str(cache), file, indent=4)


# Функция для получения данных с CoinGecko
def get_crypto_data(coin="bitcoin", currency="usd", days=200):
    # Правильные ID монет для CoinGecko
    coin_map = {
        "bnb": "binancecoin",
        "eth": "ethereum",
        "btc": "bitcoin"
    }
    coin = coin_map.get(coin, coin)  # Заменяем ID, если есть в списке

    # Загружаем кеш
    cache = load_cache()
    cache_key = f"{coin}_{days}"

    # Используем кеш, если данные уже есть
    if cache_key in cache:
        print(f"✅ Загружаем кешированные данные для {coin}")
        return pd.Series(cache[cache_key])

    # Делаем запрос к CoinGecko
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": currency, "days": days, "interval": "daily"}

    response = requests.get(url, params=params)

    # Проверяем статус ответа
    if response.status_code != 200:
        print(f"⚠️ Ошибка {response.status_code} при запросе {coin}: {response.text}")
        return pd.Series()  # Возвращаем пустую серию

    data = response.json()

    # Проверяем, есть ли "prices" в ответе
    if "prices" not in data:
        print(f"⚠️ Нет данных для {coin} в API CoinGecko!")
        return pd.Series()

    # Обрабатываем данные
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("date")["price"]

    # Сохраняем данные в кеш
    cache[cache_key] = convert_keys_to_str(df.to_dict())
    save_cache(cache)

    return df
