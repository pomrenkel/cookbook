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


#Reworked search by ingredient w/ subquery to return all ingredients for a found recipe
SELECT
    r.name,
    r.instructions,
    GROUP_CONCAT(r_ig.quantity, " ",
                 r_ig.unit, " ",
                 ig.name SEPARATOR ", ")
    AS ingredients
FROM recipes r
JOIN recipe_ingredients r_ig
    ON r.id = r_ig.recipe_id
JOIN ingredients ig
    ON r_ig.ingredient_id = ig.id
WHERE r.id IN (
        SELECT r.id FROM recipes r
        JOIN recipe_ingredients r_ig
           ON r.id = r_ig.recipe_id
        JOIN ingredients ig
            ON r_ig.ingredient_id = ig.id
        WHERE ig.name IN (ING1, ING2, ING3...)
        GROUP BY r.id
        HAVING COUNT(DISTINCT ig.name) = ING_COUNT
        )
GROUP BY r.id;

# Check for existing recipe name
SELECT
    recipes.name
FROM recipes WHERE recipes.name LIKE %s;