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
            print("\n------USER-----")
            print("Username: " + user["Username"])
            print("In visit from: " + user["In_visit_from"])
            print("In visit to: " + user["In_visit_to"])
            print("chatGptResponse: " + user["chatGptResponse"])
            print("Sex: " + user["sex"])
            print("Needs: " + user["needs"])
            print("User type: " + user["user_type"])
            print("END USER")

    def save(self):
        # Save the list of dictionaries to a csv file
        df = pd.DataFrame(self.listofUsers)
        df.to_csv('users.csv', index=False)