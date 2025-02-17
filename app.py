import sqlite3
import json
from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

# Index Page
@app.route('/')
def home():
    return render_template('index.html')

# This route gets all recipes from the databasee
@app.route('/recipes', methods=['GET'])
def get_recipe():
    if request.method == "GET":
        term = request.args.get('term', '')
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        if term == "":
            cur.execute("SELECT id, name from recipes;")
        else:
            cur.execute('''SELECT DISTINCT r.id, r.name from recipes r
                        INNER JOIN recipe_ingredients ri
                        ON ri.recipe_id = r.id
                        INNER JOIN ingredients i
                        ON i.id = ri.ingredient_id                        
                        WHERE r.name LIKE ? OR i.name LIKE ?; ''', (f"%{term}%", f'%{term}%'))

        result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

    return render_template('recipes.html', recipes = result)

# This route get all information about a recipe
@app.route('/recipes/<id>')
def get_recipe_by_id(id):
    conn = sqlite3.connect("recipes.db")
    cur = conn.cursor()
    cur.execute('''
                SELECT r.name, r.picture_url, r.instructions, measure, i.name
                FROM recipes AS r
                INNER JOIN recipe_ingredients
                ON recipe_id = r.id
                INNER JOIN ingredients AS i
                ON i.id = ingredient_id
                WHERE r.id = ?;
                ''',id)
    result = cur.fetchone()

    cur.execute('''
                SELECT measure, i.name  
                FROM recipes AS r
                INNER JOIN recipe_ingredients
                ON recipe_id = r.id
                INNER JOIN ingredients AS i
                ON i.id = ingredient_id
                where r.id = ?;
                ''',id)
    result2 = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return render_template('recipe.html', recipe_elements = result, ingredients = result2)

@app.route('/add-recipe', methods=["GET","POST"])
def add_recipe():
    if request.method == "POST":
        recipe_name = request.form['name']
        instructions = request.form['instructions']

        ingredients = json.loads(request.form['ingredients'])
        amounts = json.loads(request.form['amounts'])
        
        picture_url = request.form['picture_url']
        modified_date = request.form['modified_date']
        
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        cur.execute(''' 
        INSERT INTO recipes(name, instructions, picture_url, modified_date) 
        VALUES (?, ?, ?, ?);
        ''', (recipe_name, instructions, picture_url, modified_date))

        recipe_id = cur.lastrowid
        
        ingredient_ids= []
        for i in ingredients:
            cur.execute("INSERT INTO ingredients (name) VALUES (?);", (i,))
            ingredient_ids.append(cur.lastrowid)
        
        for i,a in zip(ingredient_ids,amounts):
            cur.execute('''INSERT INTO recipe_ingredients (recipe_id, ingredient_id, measure)
                        VALUES (?,?,?)''', (recipe_id,i,a))

        conn.commit()
        cur.close()
        conn.close()
        return render_template('add.html', message = "Recipe Added", date = date.today() )
    else:
        return render_template('add.html', message = "", date = date.today() )
    

@app.route('/edit-recipe/<id>', methods = ["GET",'POST'])
def edit_recipe(id):
    if request.method == "POST" and request.form.get("_method") != "DELETE":
        recipe_name = request.form.get('name')
        instructions = request.form.get('instructions')
        ingredients = json.loads(request.form.get('ingredients'))
        amounts = json.loads(request.form.get('amounts'))
        picture_url = request.form.get('picture_url')
        modified_date = request.form.get('modified_date')
        
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        cur.execute(''' 
        UPDATE recipes SET name = ?, instructions = ?, picture_url = ?, modified_date = ? 
        WHERE id = ?;
        ''', (recipe_name, instructions, picture_url, modified_date,id))
        
        ingredient_ids= []

        cur.execute(''' SELECT id FROM ingredients i
                    INNER JOIN recipe_ingredients ri
                    ON i.id = ri.ingredient_id
                    WHERE ri.recipe_id = ?; ''', (id))
        
        ids = cur.fetchone()

        for id in ids:
            ingredient_ids.append(id)
        
        for i, id in zip(ingredients, ingredient_ids):
            cur.execute("UPDATE ingredients SET name = ? WHERE id = ?;", (i,id))

        for i,a in zip(ingredient_ids,amounts):
            cur.execute('''
                        UPDATE recipe_ingredients SET recipe_id = ?, ingredient_id = ?, measure = ? 
                        WHERE recipe_id = ? ;
                        ''', (id, i, a, id))

        conn.commit()
        cur.close()
        conn.close()
        return render_template('index.html', message = "Recipe Modified")
    
    elif request.form.get("_method")  == "DELETE":
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        cur.executescript(f'''
                          DELETE FROM recipes WHERE id = {id};

                          DELETE FROM ingredients 
                          WHERE id IN (SELECT id FROM ingredients i
                                        INNER JOIN recipe_ingredients ri
                                        ON i.id = ri.ingredient_id
                                        WHERE ri.recipe_id = {id});

                          DELETE FROM recipe_ingredients
                          WHERE recipe_id = {id};
                          ''')
        conn.commit()
        cur.close()
        conn.close()
        return render_template('index.html', message = "Recipe Deleted", id = id)

    else:
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()
        cur.execute('''
                    SELECT r.name, r.picture_url, r.instructions, r.modified_date  
                    FROM recipes AS r
                    INNER JOIN recipe_ingredients
                    ON recipe_id = r.id
                    INNER JOIN ingredients AS i
                    ON i.id = ingredient_id
                    WHERE r.id = ?;''', id )
        result = cur.fetchone()

        cur.execute('''
                    SELECT measure, i.name  
                    FROM recipes AS r
                    INNER JOIN recipe_ingredients
                    ON recipe_id = r.id
                    INNER JOIN ingredients AS i
                    ON i.id = ingredient_id
                    where r.id = ?;
                    ''',id)
        result2 = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        return render_template('edit.html', recipe_elements = result, ingredients = result2, id = id)

if __name__ == '__main__':
    app.run(debug=True)