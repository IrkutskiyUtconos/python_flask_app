from flask import Flask

app = Flask(__name__)
app.config['DATABASE'] = 'app/recipes.db'

from app import routes