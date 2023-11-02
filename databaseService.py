import sqlite3
import pandas as pd
import re


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list

    def print(self):
        # Beautify the output of printing a list of dictionaries
        for user in self.listofUsers:
            print(user)
            print("\n")


