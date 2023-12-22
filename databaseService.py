import csv
import json


class DatabaseService:
    def __init__(self, list):
        self.listofUsers = list

    @staticmethod
    def save_post(cityQuestionedInPost, cityOfProvenanceOfUser, usernameOfUser, postText):

        # Retrieving element from a json string
        python_dict = {'text': postText, 'username': usernameOfUser, 'city_request': cityQuestionedInPost,
                       'city_provenance': cityOfProvenanceOfUser}

        # Adding city of provenance and city requested to the python dictionary
        file_name = "output_japan.csv"

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

    """
    This function saves a json string in a csv file.
    
    Parameters:
    element (json): Response from chatgpt
    cityQuestionedInPost (String): The city for which the question is asked.
    cityOfProvenanceOfUser (String): The city of provenance of the user who made the post.
    """
    @staticmethod
    def save(element, cityQuestionedInPost, cityOfProvenanceOfUser):

        # Retrieving element from a json string
        start_index = element.find('{')
        json_string = element[start_index:]
        python_dict = json.loads(json_string)

        if 'need1' not in python_dict:
            python_dict['need1'] = 'None'
        if 'need2' not in python_dict:
            python_dict['need2'] = 'None'
        if 'need3' not in python_dict:
            python_dict['need3'] = 'None'
        if 'need4' not in python_dict:
            python_dict['need4'] = 'None'

        # Adding city of provenance and city requested to the python dictionary
        python_dict['city_request'] = cityQuestionedInPost
        python_dict['city_provenance'] = cityOfProvenanceOfUser

        if python_dict['spam'].lower() not in ['yes', 'y']:
            file_name = "output_newyork.csv"

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
