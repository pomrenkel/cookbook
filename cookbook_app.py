import yaml
import mysql.connector

COMMANDS = {"i": "INSERT", "q": "QUIT", "s": "SEARCH"}


class CBController:
    def __init__(self, cfg_file_path):
        self._MyModel = CBModel(cfg_file_path)
        self._MyView = CBView()

    def test(self):
        self._MyModel.formatQuery()
        self._MyModel.execQuery()

    def processInput(self, *args):
        options = {}


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

    def formatQuery(self, *args):
        self.query = "SELECT * FROM recipes"
        pass

    def execQuery(self):
        self.cursor.execute(self.query)
        result = self.cursor.fetchall()
        for x in result:
            print(x)
        self.cursor.close()
        self.cnx.close()


class CBView:
    def __init__(self):
        self.sql_result = None
        self.formatted_out = None

    def printWelcome(self):
        print("\nWelcome to the cookbook!\n")
        self.printCommands()

    def printCommands(self):
        for k, v in COMMANDS.items():
            print(k + "\t\t\t" + v)
        print()

    def readIn(self, sql_result):
        # Processing sql results to format for outputting
        pass

    def printResults(self):
        # printing out the formatted results as specified
        pass


if __name__ == "__main__":
    myController = CBController("config.yaml")
    myController._MyView.printWelcome()
    myController.test()
