import csv
import sqlite3
import pandas as pd
import re
import ast
import json


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list


    @staticmethod
    def save(element, cityQuestionedInPost, cityOfProvenanceOfUser):

        # Retriving element from a json string
        start_index = element.find('{')
        json_string = element[start_index:]
        python_dict = json.loads(json_string)

        # Adding city of provenance and city requested to the python dictionary
        python_dict['city_request'] = cityQuestionedInPost
        python_dict['city_provenance'] = cityOfProvenanceOfUser

        if python_dict['spam'].lower() not in ['yes', 'y']:
            file_name = "output.csv"

            # Check if the file exists or create a new one with headers
            file_exists = True
            try:
                with open(file_name, 'r') as f:
                    file_exists = True
            except FileNotFoundError:
                file_exists = False

            # Open the file in append mode, if it exists, and write the data
            with open(file_name, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=python_dict.keys())

                # If the file didn't exist, write the header row
                if not file_exists:
                    writer.writeheader()

                # Write the data
                writer.writerow(python_dict)
