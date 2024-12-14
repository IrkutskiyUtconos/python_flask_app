# Recipe Finder Service

## Описание проекта

Этот сервис позволяет находить рецепты на основе заданного списка ингредиентов. Пользователь вводит ингредиенты, а сервис возвращает подходящие рецепты, используя данные, полученные с сайта **povar.ru**.

## Функциональность

- **Поиск рецептов по ингредиентам:** Введите список ингредиентов, и сервис предложит подходящие рецепты.
- **Скрапинг данных:** Сервис автоматически собирает данные с сайта povar.ru.
- **Хранение данных:** Используется база данных SQLite, которая сохраняет рецепты между перезапусками сервиса.

## Как запустить проект

### Требования

- Установленный Docker и Docker Compose.
- Git для работы с репозиторием.

### Инструкции по запуску

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/IrkutskiyUtconos/python_flask_app.git
cd your_project
```
2. **Запустите сервис:**
Выполните скрипт сборки и запуска:
```bash
./build.sh
```
3. **Откройте веб-приложение:** Перейдите в браузере по адресу https://localhost:5000. Вы сможете ввести список ингредиентов и получить подходящие рецепты.

### Обновление данных (запуск скрапера вручную)
Если нужно обновить данные в базе, выполните следующую команду:
```bash
docker-compose exec web flask scrape-and-save
```

## Как работает проект
1. **Скрапинг:** Сервис использует модуль scraper.py для получения данных с сайта povar.ru.
2. **Обработка данных:** Полученные рецепты сохраняются в базу данных SQLite.
3. **Интерфейс:** Пользователь вводит ингредиенты на веб-странице, а сервис ищет рецепты в базе.