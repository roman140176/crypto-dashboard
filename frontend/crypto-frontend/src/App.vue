<script setup>
import { ref, onMounted, computed, watch } from "vue";
import axios from "axios";
import { Chart, registerables } from "chart.js";
import { darkTheme, NConfigProvider, NSelect, NButton, NSpace, NSpin } from "naive-ui";

Chart.register(...registerables);

const coin = ref("bitcoin");
const prices = ref([]);
const sma50 = ref([]);
const sma200 = ref([]);
const ema9 = ref([]);
const ema21 = ref([]);
const chart = ref(null);
const isDark = ref(false);
const isLoading = ref(false); // Флаг загрузки

const theme = computed(() => (isDark.value ? darkTheme : null));
const gridColor = computed(() => (isDark.value ? "#444" : "#ddd"));

// Следим за темой и добавляем плавный переход
watch(isDark, (newVal) => {
  document.body.classList.add("theme-transition");
  if (newVal) {
    document.body.classList.add("dark-mode");
  } else {
    document.body.classList.remove("dark-mode");
  }
});

const coins = [
  { label: "Bitcoin", value: "bitcoin" },
  { label: "Ethereum", value: "ethereum" },
  { label: "BNB", value: "binancecoin" }
];

const fetchData = async () => {
  isLoading.value = true; // Включаем лоадер
  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/data?coin=${coin.value}`);
    prices.value = Object.entries(res.data.prices).map(([date, value]) => ({ date, value }));
    sma50.value = Object.entries(res.data.sma_50).map(([date, value]) => ({ date, value }));
    sma200.value = Object.entries(res.data.sma_200).map(([date, value]) => ({ date, value }));
    ema9.value = Object.entries(res.data.ema_9).map(([date, value]) => ({ date, value }));
    ema21.value = Object.entries(res.data.ema_21).map(([date, value]) => ({ date, value }));
    drawChart();
  } catch (err) {
    console.error("Ошибка загрузки данных", err);
  }
  isLoading.value = false; // Выключаем лоадер
};

const drawChart = () => {
  if (chart.value) chart.value.destroy();
  const ctx = document.getElementById("cryptoChart").getContext("2d");
  chart.value = new Chart(ctx, {
    type: "line",
    data: {
      labels: prices.value.map(p => p.date),
      datasets: [
        { label: "Цена", data: prices.value.map(p => p.value), borderColor: isDark.value ? "white" : "black" },
        { label: "SMA 50", data: sma50.value.map(p => p.value), borderColor: "blue", borderDash: [5, 5] },
        { label: "SMA 200", data: sma200.value.map(p => p.value), borderColor: "red", borderDash: [5, 5] },
        { label: "EMA 9", data: ema9.value.map(p => p.value), borderColor: "green" },
        { label: "EMA 21", data: ema21.value.map(p => p.value), borderColor: "purple" }
      ]
    },
    options: {
      scales: {
        x: {
          grid: { color: gridColor.value }
        },
        y: {
          grid: { color: gridColor.value }
        }
      }
    }
  });
};

onMounted(fetchData);
</script>

<template>
  <n-config-provider :theme="theme">
    <div class="container">
      <div class="header">
        <n-space>
          <n-select
            v-model:value="coin"
            :options="coins"
            placeholder="Выберите валюту"
            @update:value="fetchData"
            class="crypto-select"
          />
          <n-button @click="isDark = !isDark">
            {{ isDark ? "🌞 Светлая" : "🌙 Тёмная" }}
          </n-button>
        </n-space>
      </div>

      <!-- Показываем лоадер, если данные загружаются -->
      <n-spin v-if="isLoading" size="large" />

      <!-- График -->
      <canvas v-show="!isLoading" id="cryptoChart"></canvas>
    </div>
  </n-config-provider>
</template>

<style>
/* Анимация смены темы */
.theme-transition {
  transition: background-color 0.5s ease-in-out, color 0.5s ease-in-out;
}

/* Светлая тема */
body {
  background-color: white;
  color: black;
}

/* Тёмная тема */
body.dark-mode {
  background-color: #121212;
  color: white;
}

/* Контейнер */
.container {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
canvas {
  max-width: 100%;
  height: 400px;
}
.n-select,.n-button{
  width: 120px;
}
</style>
