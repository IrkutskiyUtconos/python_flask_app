import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_and_save(base_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить страницу: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    recipe_links = soup.find_all('a', class_='listRecipieTitle')
    recipes = []
    for link in recipe_links:
        href = link.get('href')
        name = link.text.strip()
        if href and name:
            recipes.append((f"https://povar.ru{href}", name))
    conn = sqlite3.connect('app/recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            url TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            recipe_id INTEGER,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id)
        )
    ''')
    conn.commit()
    for recipe_url, recipe_name in recipes:
        try:
            cursor.execute('INSERT OR IGNORE INTO recipes (name, url) VALUES (?, ?)', (recipe_name, recipe_url))
            conn.commit()
            cursor.execute('SELECT id FROM recipes WHERE url = ?', (recipe_url,))
            recipe_id = cursor.fetchone()[0]
            ingredients = scrape_ingredients(recipe_url)
            for ingredient in ingredients:
                cursor.execute('INSERT INTO ingredients (name, recipe_id) VALUES (?, ?)', (ingredient, recipe_id))
            conn.commit()
            print(f"Успешно добавлен рецепт: {recipe_name} с {len(ingredients)} ингредиентами.")
        except Exception as e:
            print(f"Ошибка при обработке рецепта {recipe_name}: {e}")
    conn.close()

def scrape_ingredients(recipe_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(recipe_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить рецепт: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    ingredients_block = soup.find_all('li')
    ingredients = []
    for item in ingredients_block:
        span = item.find('span', class_='name')
        if span:
            ingredients.append(span.text.strip())
    if not ingredients:
        raise Exception(f"Ингредиенты не найдены для {recipe_url}")
    return ingredients

i = 1
while i < 10:
    base_url = f"https://povar.ru/mostnew/all/{i}/"
    scrape_and_save(base_url)
    i += 1
