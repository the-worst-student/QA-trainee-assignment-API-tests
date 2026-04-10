# QA trainee assignment — API tests

## Описание

Проект содержит автотесты для API сервиса объявлений.

Покрываются следующие endpoint'ы API v1:

- `POST /api/1/item` — создание объявления
- `GET /api/1/item/{id}` — получение объявления по идентификатору
- `GET /api/1/{sellerID}/item` — получение всех объявлений продавца
- `GET /api/1/statistic/{id}` — получение статистики по объявлению

Автотесты написаны на Python с использованием `pytest` и `requests`.

---

## Структура проекта

- `config.py` — конфигурация проекта, базовый URL и timeout
- `api_client.py` — клиент для работы с API
- `build_data.py` — генерация валидных и уникальных тестовых данных
- `conftest.py` — pytest-фикстуры
- `test_items_positive.py` — позитивные сценарии
- `test_items_negative.py` — негативные сценарии
- `test_items_corner_cases.py` — corner-case сценарии
- `test_items_nonfunctional.py` — нефункциональные проверки
- `TESTCASES.md` — список тест-кейсов
- `README.md` — инструкция по запуску

---

## Используемый стек

- Python 3.12
- pytest
- requests

---

## Линтер и форматтер

В проект добавлены инструменты для проверки качества и форматирования кода:

- `ruff` — линтер для статического анализа Python-кода;
- `black` — форматтер для автоматического приведения кода к единому стилю.

Конфигурация инструментов хранится в файле `pyproject.toml`.

### Установка

Если зависимости ещё не установлены, выполните:


## Установка зависимостей

```
git clone https://github.com/the-worst-student/QA-trainee-assignment-API-tests.git
cd QA-trainee-assignment-API-tests
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest
```

Запуск конкретного файла с тестами:
```
pytest test_items_positive.py
pytest test_items_negative.py
pytest test_items_corner_cases.py
pytest test_items_nonfunctional.py
```

Полный прогон с автоисправлением и автоформатированием:
```
ruff check . --fix
black .
pytest
```
