import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

conn = sqlite3.connect("recipes.db")
cur = conn.cursor()


@app.route('/')
def home():
    #return "Hello world from Flask"
    return render_template('index.html')

@app.route('/add-recipe')
def add_recipe():
    return render_template('add.html')

@app.route('/edit-recipe/<name>')
def edit_recipe(name):

    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)