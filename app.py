import sqlite3
from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

# Index Page
@app.route('/')
def home():
    return render_template('index.html')

# This route gets all rexipes from the databasee
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
                        WHERE r.name LIKE ? OR i.name LIKE ?; ''', ('%' + term + '%', term + '%'))

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
        recipe_name = request.form['recipe']
        instructions = request.form['instructions']
        picture_url = request.form['picture_url']
        modified_date = request.form['modified_date']
        
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        cur.execute(''' INSERT INTO recipes(name,instructions,picture_url,modified date) 
                          VALUES ({recipe_name},{instructions},{picture_url},{modified_date});
                          ''')
        
        cur.execute("INSERT INTO ingredients(name)VALUES ({});")

        cur.execute('''
                    INSERT INTO recipe_ingredients(recipe_id, ingredient_id, {});
                    SELECT r.id, i.id,  
                    FROM recipes AS r
                    INNER JOIN recipe_ingredients
                    ON recipe_id = r.id
                    INNER JOIN ingredients AS i
                    ON i.id = ingredient_id
                    WHERE r.name = {recipe_name} AND i.name = {};
                    ''')

        conn.commit()
        cur.close()
        conn.close()
        return render_template('add.html', message = "Recipe Added", date = date.today() )
    else:
        return render_template('add.html', message = "", date = date.today() )
    

@app.route('/edit-recipe/<id>', methods = ["GET","POST","DELETE"])
def edit_recipe(id):
    if request.method == "POST":
        return render_template('edit.html')

    elif request.method == "DELETE":
        conn = sqlite3.connect("recipes.db")
        cur = conn.cursor()

        cur.executescript('''
                          DELETE * FROM recipes WHERE id = ?;

                          DELETE * FROM ingredients i
                          INNER JOIN recipe_ingredients ri
                          ON ri.ingredients_id = id
                          WHERE ri.ingredients_id = ?;
                          ''', id)
        conn.commit()
        cur.close()
        conn.close()

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
        return render_template('edit.html', recipe_elements = result, ingredients = result2)


# @app.route('/delete-recipe/<id>', methods = ["DELETE"])
# def delete_recipe(id):
#     conn = sqlite3.connect("recipes.db")
#     cur = conn.cursor()
#     cur.execute('''
#                 SELECT r.name, r.picture_url, r.instructions, measure, i.name, r.modified_date  
#                 FROM recipes AS r
#                 INNER JOIN recipe_ingredients
#                 ON recipe_id = r.id
#                 INNER JOIN ingredients AS i
#                 ON i.id = ingredient_id
#                 WHERE r.id = ?;''', id )
#     result = cur.fetchone()

#     cur.execute('''
#                 SELECT measure, i.name  
#                 FROM recipes AS r
#                 INNER JOIN recipe_ingredients
#                 ON recipe_id = r.id
#                 INNER JOIN ingredients AS i
#                 ON i.id = ingredient_id
#                 where r.id = ?;
#                 ''',id)
#     result2 = cur.fetchall()

#     conn.commit()
#     cur.close()
#     conn.close()
#     return render_template('edit.html', recipe_elements = result, ingredients = result2)

if __name__ == '__main__':
    app.run(debug=True)