import sqlite3
import pandas as pd
import re
import ast
import json

csv_filename = "output_crawler.csv"


def write_row(my_string):
    # The name of the CSV file where the string will be written
    csv_filename = "output_crawler.csv"

    # Open the file in write mode ('w') and create a csv.writer object
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csvfile.write(my_string + '\n')


def parse_input_to_csv(input_str):
    print("Current string: \n" + input_str)
    try:
        # Analisi dell'input come un dizionario
        data = json.loads(input_str)

        # Controlla se il campo SPAM è falso o simile
        spam = data.get('spam', '')
        if isinstance(spam, bool):
            if (spam):
                print("spam")
                return "spam"
        try:
            if 'true' in spam or 'http' in spam or 'yes' in spam:
                print("spam")
                return "spam"
        except Exception as e:
            print("error: ", e)
            pass

        # Estrazione dei campi richiesti
        sex = data.get('sex', '')
        users = data.get('user', '')
        needs = data.get('need', '')

        # Gestisce sia i dizionari Need sia le stringhe singole
        if isinstance(needs, dict):
            need_values = [needs.get(f'need{i}', '') for i in range(1, len(needs) + 1)]
        elif isinstance(needs, list):
            need_values = needs
        else:
            need_values = [needs]

        if isinstance(users, dict):
            user_values = [users.get(f'user{i}', '') for i in range(1, len(users) + 1)]
        elif isinstance(users, list):
            user_values = users
        else:
            user_values = [users]


        # Creazione della stringa CSV
        csv_str = ','.join([sex] + user_values + need_values)
        return csv_str

    except json.JSONDecodeError:
        # Gestisce errori di formattazione
        return "Errore di formattazione"


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list

    @staticmethod
    def extend(cityQuestionedInPost, cityOfProvenanceOfUser, usernameOfUser, postText, responseFromChatGpt):

        city_request = cityQuestionedInPost
        city_provenance = cityOfProvenanceOfUser
        username = usernameOfUser
        postText = postText

        clean_string = str(responseFromChatGpt)[11:]
        clean_string = clean_string.replace('python', '')
        clean_string = clean_string.replace('`', '')
        clean_string = clean_string.lower()
        clean_string = clean_string.replace('\n', '')
        clean_string = clean_string.replace('\t', '')
        clean_string = re.sub(' +', ' ', clean_string)

        x = parse_input_to_csv(clean_string)
        if x != "spam":
            x = x.replace('"', '')
            print(x)
            write_row(city_request+','+city_provenance+','+username+','+x)
        else:
            print("spam")
