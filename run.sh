#!/bin/bash
cd "$(dirname "$0")"  # Переход в папку скрипта
source venv/bin/activate  # Активируем виртуальное окружение
python3 src/main.py "$@"  # Запускаем парсер с аргументами
