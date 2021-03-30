import os
import sys
import yaml
import mysql.connector

COMMANDS = {"i": "INSERT", "q": "QUIT", "s": "SEARCH"}


class CBController:
    def __init__(self, cfg_file_path):
        self._MyModel = CBModel(cfg_file_path)
        self._MyView = CBView()

    def test(self):
        """Test method for running and printing output of a simple SELECT * in the test db"""
        self._MyModel.formatQuery()
        self._MyModel.execQuery()

    def processInput(self):  # TODO: cleaning input, parsing for optionals, and passing to correct command
        raw_input = input("Waiting for input: ")
        result_list = raw_input.strip().lower().split()

        # Verification portion of the processing - raising exceptions here if errors
        if result_list[0] not in COMMANDS:
            raise KeyError("Please enter a valid command.")
        else:
            command = COMMANDS[result_list[0]]



        #Analyzing list input for validity

        #If correct, passing list input to correct command


    def eventLoop(self):
        while True:
            try:
                self.processInput()
            except KeyError:
                print("Please enter a valid command")
            return

            # user_in = input("Waiting for input: ").lower()
            # if user_in == "q":
            #     print("Exiting")
            #     return
            # elif user_in in COMMANDS:
            #     print(f"You chose {COMMANDS[user_in]}")
            # else:
            #     print("Please enter a valid command")
            #     self._MyView.printCommands()


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
        self.sql_result = None # Raw response
        self.formatted_out = None # Printing out just what needed

    def printWelcome(self):
        """Prints out the program initial welcome message"""
        print("\nWelcome to the cookbook!\n")
        self.printCommands()

    @staticmethod
    def printCommands():
        """Prints out command keys and their respective command"""
        for k, v in COMMANDS.items():
            print(k + "\t\t\t" + v)
        print()

    def formatResults(self, sql_result):
        """Formats raw SQL results and stores raw/formatted of most recent result"""
        pass

    def printResults(self):
        """Displays formatted SQL results to user"""
        # printing out the formatted results as specified
        pass


if __name__ == "__main__":
    myController = CBController("config.yaml")  # TODO: Add config file selection as first separate step
    myController._MyView.printWelcome()
    myController.eventLoop()
    myController.test()
