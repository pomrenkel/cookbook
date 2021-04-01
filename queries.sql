# noinspection SqlResolveForFile

#Search by recipe name query
SELECT
  recipes.name,
  instructions,
  GROUP_CONCAT(quantity, " ", unit, " ", ingredients.name SEPARATOR ', ') AS ingredients
FROM recipes
LEFT JOIN recipe_ingredients
  ON recipes.id = recipe_ingredients.recipe_id
LEFT JOIN ingredients
  ON recipe_ingredients.ingredient_id = ingredients.id
WHERE recipes.name LIKE RECIPE_NAME
GROUP BY recipes.name;


#Search by recipe ingredient query
SELECT
    recipes.name,
    recipes.instructions,
    GROUP_CONCAT(recipe_ingredients.quantity, " ",
                 recipe_ingredients.unit, " ",
                 ingredients.name SEPARATOR ", ")
    AS ingredients
FROM recipes
JOIN recipe_ingredients
    ON recipes.id = recipe_ingredients.recipe_id
JOIN ingredients
    ON recipe_ingredients.ingredient_id = ingredients.id
WHERE ingredients.name IN (ing1, ing2, ing3, ing4, ...)
GROUP BY recipes.name
HAVING COUNT(DISTINCT ingredients.name) = TOTAL_ING_NUMBER;