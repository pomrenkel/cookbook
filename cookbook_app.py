import os
import sys
import yaml
import mysql.connector

COMMANDS = {"i": "INSERT", "q": "QUIT", "s": "SEARCH"}


class CBController:
    def __init__(self, cfg_file_path):
        self._MyModel = CBModel(cfg_file_path)
        self._MyView = CBView()

    def processInput(self):  # TODO: cleaning input, parsing for optionals, and passing to correct command
        raw_input = input("Waiting for input: ")
        result_list = raw_input.strip().lower().split()

        # Verification portion of the processing - raising exceptions here if errors
        if not result_list or result_list[0] not in COMMANDS:
            raise KeyError("Please enter a valid command.")
        else:
            command = COMMANDS[result_list[0]]

        # TODO: Add checking for necessary search keywords

        if command == COMMANDS["s"]:
            self._MyModel.searchQuery(name="chicken parmesan") #TODO: Add input formatting to produce list
        elif command == COMMANDS["q"]:
            self._MyModel.safeClose()

        # Analyzing list input for validity

        # If correct, passing list input to correct command

    def eventLoop(self):
        while True:
            try:
                self.processInput()
            except KeyError:
                print("Please enter a valid command")


class CBModel:
    def __init__(self, file_path):
        self.cfg = self.loadConfig(file_path)
        self.cnx = mysql.connector.connect(**self.cfg['database'])
        self.cursor = self.cnx.cursor()
        self.query = ""

    @staticmethod
    def loadConfig(file_path):
        """Returns config dict object from given filepath"""
        try:
            with open(file_path, "r") as cfg_file:
                cfg = yaml.safe_load(cfg_file)
        except FileNotFoundError:
            print(f"Could not find file: {file_path}")
        else:
            print("*** Config file found. ***")
            return cfg

    def searchQuery(self, name=None, ingredients=None):
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

            self.execQuery(data=(name,))

        elif ingredients:

            dynamic_query = ", ".join(["%s"] * len(ingredients))
            dynamic_count = len(ingredients)

            self.query = f"""SELECT
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
                            WHERE ingredients.name IN ({dynamic_query})
                            GROUP BY recipes.name
                            HAVING COUNT(DISTINCT ingredients.name) = {dynamic_count}"""

            self.execQuery(data=ingredients)
            #first is comma-separated sequence of ingredient names, 2nd is # of ingredients

        #search by ingredients

    def execQuery(self, data=None):
        self.cursor.execute(self.query, data)
        result = self.cursor.fetchall() # assigns list of results to result
        for recipe, instr, ingr in result:
            print(f"Recipe: {recipe} \nInstructions: {instr} \nIngredients: {ingr}")

    def safeClose(self):
        self.cursor.close()
        self.cnx.close()
        print("Closing cookbook.")
        sys.exit()


class CBView:
    def __init__(self):
        self.sql_result = None  # Raw response
        self.formatted_out = None  # Printing out just what needed

    def printWelcome(self):
        """Prints out the program initial welcome message"""
        print("\nWelcome to the cookbook!\n")
        self.printCommands()

    @staticmethod
    def printCommands():
        """Prints out command keys and their respective command"""
        for k, v in COMMANDS.items():
            print(f"{k} \t \t {v}")
        print()

    def formatResults(self, sql_result):
        """Formats raw SQL results and stores raw/formatted of most recent result"""
        pass

    def printResults(self):
        """Displays formatted SQL results to user"""
        # printing out the formatted results as specified
        pass


if __name__ == "__main__":
    myController = CBController("config.yaml")  # TODO: Add config file selection as first separate step (creation function)
    myController._MyView.printWelcome() #TODO: Repackage this into myController
    myController.eventLoop()
