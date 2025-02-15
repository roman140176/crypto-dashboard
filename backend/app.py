from flask import Flask, jsonify, request
from flask_cors import CORS
from fetch_data import get_crypto_data
from indicators import calculate_sma, calculate_ema

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})   # Разрешаем запросы с фронта


@app.route("/api/data", methods=["GET"])
def get_data():
    coin = request.args.get("coin", "bitcoin")

    # Получаем данные
    crypto_data = get_crypto_data(coin)
    sma_50 = calculate_sma(crypto_data, 50)
    sma_200 = calculate_sma(crypto_data, 200)
    ema_9 = calculate_ema(crypto_data, 9)
    ema_21 = calculate_ema(crypto_data, 21)

    # Формируем JSON-ответ
    response = {
        "prices": crypto_data.to_dict(),
        "sma_50": sma_50.dropna().to_dict(),
        "sma_200": sma_200.dropna().to_dict(),
        "ema_9": ema_9.dropna().to_dict(),
        "ema_21": ema_21.dropna().to_dict()
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
