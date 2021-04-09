import sys
import yaml
import mysql.connector

COMMANDS = {"i": "INSERT", "q": "QUIT", "s": "SEARCH", "h": "HELP"}
COMMANDS_HELP = {"i": ["INSERT --- insert a new recipe"],
                 "q": ["QUIT --- quit the program"],
                 "s": ["SEARCH --- search for recipes", "-i --- search by ingredients", "-n --- search by name"],
                 "h": ["HELP --- print all commands and options"]}


def choose_config():
    #If not found, ask user for config file name
    #If still not found, provide error message and request to move to current directory
    pass


class CBController:
    def __init__(self, cfg_file_path):
        self._MyModel = CBModel(cfg_file_path)
        self._MyView = CBView()
        self._MyView.print_welcome()

    def process_input(self):  # TODO: Add detection of multi-word ingredients, clean up/tighten the parsing (regex?)
        raw_input = input("Waiting for input: ")
        result_list = raw_input.strip().lower().split()

        # Verification portion of the processing - raising exceptions here if errors
        if not result_list or result_list[0] not in COMMANDS:
            raise KeyError("Please enter a valid command.")
        else:
            command = COMMANDS[result_list[0]]

        if command == COMMANDS["s"]:
            try:
                if result_list[1] == "-i":
                    result = self._MyModel.search_query(ingredients=result_list[2:])
                    self._MyView.receive_results(result)
                elif result_list[1] == "-n":
                    result = self._MyModel.search_query(name=result_list[2])
                    self._MyView.receive_results(result)
                else:
                    print("Please choose one of the given search options (-i or -n) --- see h : HELP for more info")
            except IndexError:
                print("Please enter a valid search option (-i or -n) --- see h  :  HELP for more information")
        elif command == COMMANDS["q"]:
            self._MyModel.safe_close()
        elif command == COMMANDS["h"]:
            self._MyView.print_help()
        elif command == COMMANDS["i"]:
            self.run_insert()

    def run_insert(self):
        recipe_name = input("Enter the name of your recipe: ").strip()

        if self._MyModel.check_recipe_name(recipe_name): # Breaking early if recipe exists
            print("Sorry - that recipe already exists!")
            return

        recipe_instructions = input("Please type or copy/paste the recipe instructions: ")

        print("Please enter your ingredients 1-by-1 as follows: AMOUNT;UNIT;INGREDIENT NAME")
        print("Example: 2;cup(s);breadcrumbs    OR    1.25;tablespoons;vanilla")
        print("To end ingredient entry, simply enter 'X'")

        ing_entry = ""
        recipe_ingredients = []
        while ing_entry != 'X':
            ing_entry = input().upper().strip()
            if ing_entry != 'X':
                recipe_ingredients.append(tuple(ing_entry.split(sep=";")))

        print("Is this recipe correct?")
        print(recipe_name, recipe_instructions, *recipe_ingredients, sep='\n')

        #Ask user for ingredients - check against DB for needed insertion
        #Ask user for

    def event_loop(self):
        while True:
            try:
                self.process_input()
            except KeyError:
                print("Please enter a valid command")


class CBModel:
    def __init__(self, file_path):
        self.cfg = self.load_config(file_path)
        self.cnx = mysql.connector.connect(**self.cfg['database'])
        self.cursor = self.cnx.cursor()
        self.query = ""

    @staticmethod
    def load_config(file_path):
        """Returns config dict object from given filepath"""
        try:
            with open(file_path, "r") as cfg_file:
                cfg = yaml.safe_load(cfg_file)
        except FileNotFoundError:
            print(f"Could not find file: {file_path}")
        else:
            print("*** Config file found. ***")
            return cfg

    def search_query(self, name=None, ingredients=None):
        """formats search query for name of recipe or included ingredients and calls execQuery with query"""
        if name:
            self.query = """
            SELECT
            recipes.name,
            instructions,
            GROUP_CONCAT(quantity, " ", unit, " ", ingredients.name SEPARATOR ', ') AS ingredients
            FROM recipes
            LEFT JOIN recipe_ingredients
                ON recipes.id = recipe_ingredients.recipe_id
            LEFT JOIN ingredients
                ON recipe_ingredients.ingredient_id = ingredients.id
            WHERE recipes.name LIKE %s
            GROUP BY recipes.name"""

            param = f"%{name}%"
            query_result = self.exec_query(data=(param,))

        elif ingredients:
            # search by ingredients
            dynamic_query = ", ".join(["%s"] * len(ingredients))
            dynamic_count = len(ingredients)
            self.query = f"""
            SELECT   r.name,
                     r.instructions,
                     group_concat(r_ig.quantity, " ", r_ig.unit, " ", ig.name SEPARATOR ", ") AS ingredients
            FROM     recipes r
            JOIN     recipe_ingredients r_ig
            ON       r.id = r_ig.recipe_id
            JOIN     ingredients ig
            ON       r_ig.ingredient_id = ig.id
            WHERE    r.id IN
                     (
                              SELECT   r.id
                              FROM     recipes r
                              JOIN     recipe_ingredients r_ig
                              ON       r.id = r_ig.recipe_id
                              JOIN     ingredients ig
                              ON       r_ig.ingredient_id = ig.id
                              WHERE    ig.name IN ({dynamic_query})
                              GROUP BY r.id
                              HAVING   count(DISTINCT ig.name) = {dynamic_count} )
            GROUP BY r.id
            """
            query_result = self.exec_query(data=ingredients)
        return query_result

    def exec_query(self, data=None):
        self.cursor.execute(self.query, data)
        exec_result = self.cursor.fetchall()  # assigns list of results to result
        return exec_result

    def check_recipe_name(self, recipe_name):
        """Checks for existence of a recipe by name w/in DB and returns true if found, false otherwise."""
        self.query = f"""
        SELECT 
        recipes.name
        FROM recipes WHERE recipes.name LIKE %s 
        """
        if self.exec_query(data=(recipe_name,)):
            return True
        else:
            return False

    def safe_close(self):
        self.cursor.close()
        self.cnx.close()
        print("Closing cookbook.")
        sys.exit()


class CBView:
    def __init__(self):
        self.sql_result = None  # Raw response
        self.formatted_out = None  # Printing out just what needed
        self.result_index = 0

    def print_welcome(self):
        """Prints out the program initial welcome message"""
        print("\nWelcome to the cookbook!\n")
        self.print_help()

    @staticmethod
    def print_help():
        print()
        for k, v in COMMANDS_HELP.items():
            print(f"{k} : " + "\n\t".join(v))
        print()

    def receive_results(self, sql_result_list):
        # If - Checking/error raising
        self.sql_result = sql_result_list
        self.format_results(sql_result_list)
        self.print_results()

    def format_results(self, sql_result_list):
        """Formats raw SQL results and stores formatted of most recent result"""
        # TODO: Add formatting
        self.formatted_out = sql_result_list

    def print_results(self):
        """Displays formatted SQL results to user"""
        if not self.formatted_out:
            print("No matches found.")
        else:
            for recipe, instr, ingr in self.formatted_out:
                print(f"\nRecipe: {recipe} \nInstructions: {instr} \nIngredients: {ingr}\n")

    def change_page(self, direction):
        # Receive direction and adjust display pagination
        pass


if __name__ == "__main__":
    # TODO: Add config file selection as first separate step (creation function)
    myController = CBController("config.yaml")
    myController.event_loop()
