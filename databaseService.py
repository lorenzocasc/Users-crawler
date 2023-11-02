import sqlite3
import pandas as pd
import re


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list

    def extend(self):
        # Extend the list of dictionaries with the chatGptResponse
        for user in self.listofUsers:
            text = user["chatGptResponse"]
            pattern = r"Sex: (.*?), Need: (.*?), User: (.*?)\."
            matches = re.findall(pattern, text)

            for match in matches:
                sex, need, user_type = match
                user["sex"] = sex
                user["needs"] = need
                user["user_type"] = user_type

    def print(self):
        for user in self.listofUsers:
            print(user["Username"])
            print(user["In_visit_from"])
            print(user["In_visit_to"])
            print(user["chatGptResponse"])
            print(user["sex"])
            print(user["needs"])
            print(user["user_type"])
