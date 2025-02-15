import sqlite3

conn = sqlite3.connect("recipes.db")

cursor = conn.cursor()

# Creating database tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS  recipes(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    instructions TEXT NOT NULL,
    picture_url TEXT,
    modified_date TEXT
);
""")
               
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
); 
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    measure TEXT,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
);
""")

# Inserting data into database

cursor.executescript("""
INSERT INTO recipes (id,name,picture_url,instructions,modified_date) 
    VALUES
    (1,"Big Mac","https://www.themealdb.com/images/media/meals/urzj1d1587670726.jpg","For the Big Mac sauce, combine all the ingredients in a bowl, season with salt and chill until ready to use.\r\n2. To make the patties, season the mince with salt and pepper and form into 4 balls using about 1/3 cup mince each. Place each onto a square of baking paper and flatten to form into four x 15cm circles. Heat oil in a large frypan over high heat. In 2 batches, cook beef patties for 1-2 minutes each side until lightly charred and cooked through. Remove from heat and keep warm. Repeat with remaining two patties.\r\n3. Carefully slice each burger bun into three acrossways, then lightly toast.\r\n4. To assemble the burgers, spread a little Big Mac sauce over the bottom base. Top with some chopped onion, shredded lettuce, slice of cheese, beef patty and some pickle slices. Top with the middle bun layer, and spread with more Big Mac sauce, onion, lettuce, pickles, beef patty and then finish with more sauce. Top with burger lid to serve.\r\n5. After waiting half an hour for your food to settle, go for a jog.","2025-02-11"),
    (2,"Corn Flakes with Milk", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Kellogg%27s_Corn_Flakes%2C_with_milk.jpg/1024px-Kellogg%27s_Corn_Flakes%2C_with_milk.jpg?20220423212036","Pour the cornflakes into a bowl.Top with your favorite Emborg Low Fat Milk. Serve with a spoon and enjoy!","2025-02-14");
                     
INSERT INTO ingredients (id,name) 
    VALUES
    (1,"Minced Beef"),
    (2,"Olive Oil"),
    (3,"Sesame Seed Burger Buns"),
    (4,"Onion"),
    (5,"Iceberg Lettuce"),
    (6,"Cheese"),
    (7,"Dill Pickles"),
    (8,"Mayonnaise"),
    (9,"White Wine Vinegar"),
    (10,"Pepper"),
    (11,"Mustard"),
    (12,"Onion Salt"),
    (13,"Garlic Powder"),
    (14,"Paprika"),
    (15,"Milk"),
    (16,"CornFlakes");
INSERT INTO recipe_ingredients (recipe_id,ingredient_id,measure) 
    VALUES
    (1,1,"400g"),
    (1,2,"2 tbs"),
    (1,3,"2"),
    (1,4,"Chopped"),
    (1,5,"1/4 "),
    (1,6,"2 sliced"),
    (1,7,"2 large"),
    (1,8,"1 cup "),
    (1,9,"2 tsp"),
    (1,10,"Pinch"),
    (1,11,"2 tsp"),
    (1,12,"1 1/2 tsp "),
    (1,13,"1 1/2 tsp "),
    (1,14,"1/2 tsp"),
    (2,15,"1 L"),
    (2,16,"100g");
""")

conn.commit()

cursor.close()  # It's a good practice to close the cursor
conn.close()  # And to close the connection to the database