# Overview

This is a simple recipe book web application built using Python and Flask. The application allows users to store, retrieve, and delete recipes. The data is stored in a SQLite relational database, which the app interacts with to perform operations like searching for recipes, adding new recipes, and removing old ones. The application purpose was to test SQLite database and integrate it to an application to perform CRUD operations.

**To use the program:**

1. Make sure you have Python and Flask installed.
2. Run the db.py file inside the database folder to set up the SQLite database and populate it with sample data.
3. Start the Flask application by running the app.py to launch the web server.

**Use the application by:**

- Clicking on the “Find Meal” button to view all available recipes.
- Searching for a specific recipe by typing in the search bar.
- Adding a new recipe by clicking the “Add Meal” button, where you can input the recipe's details.

# Relational Database

For this project, I used SQLite as my database engine because I wanted to learn about its characteristics and experiment with features like portability and being lightweight, which are useful for this small-scale project. I use the database to store diverse data about recipes, split into three tables.

The database structure consists of three tables: one stores the recipe ingredients, another stores the recipe details, and the last stores the relationship between recipes and ingredients, including the amount of each ingredient.

**Recipes**

- id (INTEGER, Primary Key)
- name (TEXT)
- picture_url (TEXT)
- instructions (TEXT)
- modified_date (TEXT)

**Ingredients**

- id (INTEGER, Primary Key)
- name (TEXT)

**Recipe_ingredients**

- recipe_id (INTEGER, Foreign Key referencing recipes.id)
- ingredient_id (INTEGER, Foreign Key referencing ingredients.id)
- measure (TEXT)

# Development Environment

**Tools**

- Visual Studio Code

**Programming Languages and Libraries**

- Python
  - Python Standard Library
    - SQLite3: Used to interact with SQLite database and perform CRUD operations.
    - Json: Handle Json returned by HTML forms.
    - date: Retrieve the date recipe was modified.
  - Flask Python Framework: It was used for building the web application and handle HTTP requests
- JavaScript
- CSS
  - Water.css CSS library for general styling

# Useful Websites

- [Python documentation](https://docs.python.org/3/library/sqlite3.html#module-sqlite3)
- [w3schools SQL Tutorial](https://www.w3schools.com/sql/default.asp)
- [MDN web docs](https://developer.mozilla.org/en-US/docs/Web)
- [Learn Flask for Python - Full Tutorial](https://www.youtube.com/watch?v=Z1RJmh_OqeA&t=1312s)

# Future Work

- Add form validation
- Feature: Edit number of ingredients after insertion
