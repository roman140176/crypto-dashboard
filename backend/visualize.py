import matplotlib

matplotlib.use("TkAgg")  # Указываем бэкенд TkAgg
import matplotlib.pyplot as plt


def plot_chart(crypto_data, sma_50, sma_200, ema_9, ema_21, title):
    plt.figure(figsize=(12, 6))
    plt.plot(crypto_data, label="Цена", color="black", linewidth=1)
    plt.plot(sma_50, label="SMA 50", linestyle="dashed", color="blue")
    plt.plot(sma_200, label="SMA 200", linestyle="dashed", color="red")
    plt.plot(ema_9, label="EMA 9", linestyle="solid", color="green")
    plt.plot(ema_21, label="EMA 21", linestyle="solid", color="purple")

    plt.title(title)
    plt.xlabel("Дата")
    plt.ylabel("Цена (USD)")
    plt.legend()
    plt.grid()
    plt.show()
