from flask import render_template, request, jsonify
from app import app
from app.database import get_db_connection

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/recipes/<int:id>')
def recipe_details(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    ingredients = conn.execute('''
        SELECT ingredients.name 
        FROM ingredients 
        WHERE ingredients.recipe_id = ?
    ''', (id,)).fetchall()
    conn.close()
    if recipe is None:
        return "Рецепт не найден", 404
    return render_template('recipe_details.html', recipe=recipe, ingredients=ingredients)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            return render_template('search.html', error="Введите хотя бы один ингредиент.")
        ingredients = [ing.strip() for ing in query.split(',') if ing.strip()]
        if not ingredients:
            return render_template('search.html', error="Введите хотя бы один ингредиент.")
        query_parts = " OR ".join(["ingredients.name LIKE ?" for _ in ingredients])
        query = f'''
            SELECT recipes.id, recipes.name
            FROM recipes
            JOIN ingredients ON recipes.id = ingredients.recipe_id
            WHERE {query_parts}
            GROUP BY recipes.id
        '''
        params = [f"%{ing}%" for ing in ingredients]
        conn = get_db_connection()
        recipes = conn.execute(query, params).fetchall()
        conn.close()
        if not recipes:
            return render_template('search_results.html', recipes=None, query=query)
        return render_template('search_results.html', recipes=recipes, query=', '.join(ingredients))
    return render_template('search.html')
