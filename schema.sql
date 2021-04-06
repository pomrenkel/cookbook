# noinspection SqlIdentifierLengthForFile

# noinspection SqlResolveForFile

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
("Chicken Parmesan", "1) Bread the chicken. 2) Bake the chicken. 3) Top on pasta."), #1
("Pizza", "1) Roll out your dough. 2) Top with cheese and toppings. 3) Bake at 350 for 40 minutes."), #2
("Toast", "1) Put toast in toaster for a few minutes. 2) Butter that bitch. 3) Cronch cronch."), #3
("Blueberry Muffins", "1) Mix flour and eggs. 2) Add blueberries. 3) Bake in oven. 4) Let cool."); #4


INSERT INTO ingredients(name) VALUES
("chicken"),  #1
("breadcrumbs"), #2
("marinara sauce"), #3
("flour"), #4
("blueberry"), #5
("bread"), #6
("eggs"), #7
("shredded cheese"), #8
("butter"), #9
("pepperoni"); #10

INSERT INTO recipe_ingredients(quantity, unit, recipe_id, ingredient_id) VALUES
(3, "breasts", 1, 1),
(1, "cup(s)", 1, 2),
(2, "cup(s)", 1, 3),
(.5, "cup(s)", 1, 4),
(1, "cup(s)", 2, 4),
(1, "cup(s)", 2, 3),
(2.5, "cup(s)", 2, 8),
(1, "handful", 2, 10),
(2, "slices", 3, 6),
(1, "pat", 3, 9),
(1.5, "cup(s)", 4, 4),
(4, "whole", 4, 7),
(.75, "cup(s)", 4, 5);
