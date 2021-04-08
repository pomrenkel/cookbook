import sys
import yaml
import mysql.connector

COMMANDS = {"i": "INSERT", "q": "QUIT", "s": "SEARCH", "h": "HELP"}
COMMANDS_HELP = {"i": ["INSERT --- insert a new recipe"],
                 "q": ["QUIT --- quit the program"],
                 "s": ["SEARCH --- search for recipes", "-i --- search by ingredients", "-n --- search by name"],
                 "h": ["HELP --- print all commands and options"]}


def choose_config():
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
            except IndexError:
                print("Please enter a valid search option (-i or -n) --- see h  :  HELP for more information")
        elif command == COMMANDS["q"]:
            self._MyModel.safe_close()
        elif command == COMMANDS["h"]:
            self._MyView.print_help()

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
            self.query = """SELECT
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
