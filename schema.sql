
DROP DATABASE IF EXISTS cb_test;
CREATE DATABASE cb_test;
USE cb_test;

CREATE TABLE recipes(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  instructions TEXT NOT NULL
);

CREATE TABLE ingredients(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE recipe_ingredients(
  quantity DECIMAL(6,2) NOT NULL,
  unit VARCHAR(40),
  recipe_id INT,
  ingredient_id INT,
  FOREIGN KEY(recipe_id) REFERENCES recipes(id),
  FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
);


INSERT INTO recipes(name, instructions) VALUES
("Chicken Parmesan", "1) Bread the chicken. 2) Bake the chicken. 3) Top on pasta."),
("Muffins", "1) Make the batter. 2) Bake in oven. 3) Enjoy!"),
("Pizza", "1) Roll out your dough. 2) Top with cheese and toppings. 3) Bake at 350 for 40 minutes."),
("Toast", "1) Put toast in toaster for a few minutes. 2) Spread preferred topping and enjoy.");


INSERT INTO ingredients(name) VALUES
("chicken"),
("breadcrumbs"),
("marinara sauce"),
("flour"),
("blueberry"),
("bread");

INSERT INTO recipe_ingredients(quantity, unit, recipe_id, ingredient_id) VALUES
(3, "breasts", 1, 1),
(1, "cup(s)", 1, 2),
(2, "cup(s)", 1, 3),
(2, "slices", 4, 6);

SELECT
  recipes.name,
  instructions,
  CONCAT(quantity, " ", unit, " ", ingredients.name) AS ingredient
FROM recipe_ingredients
INNER JOIN recipes
  ON recipe_ingredients.recipe_id = recipes.id
INNER JOIN ingredients
  ON recipe_ingredients.ingredient_id = ingredients.id;
