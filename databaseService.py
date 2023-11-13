import sqlite3
import pandas as pd
import re
import ast


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list

    def extend(self):
        # Extend the list of dictionaries with the chatGptResponse
        # Save the list of dictionaries to a csv file
        assistant_pattern = re.compile(r'assistant: ({.*?})')

        # Search for the assistant dictionary in the text





    def save(self):
        df = pd.DataFrame(self.listofUsers)
        df.to_csv('users.csv', index=False)
