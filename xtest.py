# import json
# import os
# import re
# os.system('clear')

# def parse_input_to_csv(input_str):
#     print("Current string: \n"+input_str)
#     try:
#         # Analisi dell'input come un dizionario
#         data = json.loads(input_str)

#         # Controlla se il campo SPAM è falso o simile
#         spam = data.get('Spam', '').lower()
#         if 'true' in spam or 'http' in spam or 'yes' in spam:
#             print("SPAM")
#             return "SPAM"

#         # Estrazione dei campi richiesti
#         sex = data.get('Sex', '')
#         users = data.get('User', '')
#         needs = data.get('Need', '')
#         print("type(users)",type(users))
#         print("type(needs)",type(needs))

#         need_values1 = []
#         user_values1 = []


#         # Gestisce sia i dizionari Need sia le stringhe singole
#         if isinstance(needs, dict):
#             need_values = [needs.get(f'need{i}', '') for i in range(1, len(needs) + 1)]
#             need_values1 = [needs.get(f'Need{i}', '') for i in range(1, len(needs) + 1)]
#         else:
#             need_values = [needs]
        
#         if isinstance(users, dict):
#             user_values = [users.get(f'user{i}', '') for i in range(1, len(users) + 1)]
#             user_values1 = [users.get(f'User{i}', '') for i in range(1, len(users) + 1)]
#         else:
#             user_values = [users]


#         print("user_values",user_values, user_values1)
#         print("need_values",need_values, need_values1)
        
#         # Creazione della stringa CSV
#         csv_str = ','.join([sex] + user_values + user_values1 + need_values + need_values1)

#         csv_str = re.sub(r',+', ',', csv_str)
#         return csv_str

#     except json.JSONDecodeError:
#         # Gestisce errori di formattazione
#         return "Errore di formattazione"
    




# text = "{\
#   \"Sex\": \"Female\",\
#   \"Need\": {\
#     \"need1\": \"Interest in attending international sporting events (specifically tennis)\",\
#     \"need2\": \"Engagement in local events and exhibitions\",\
#     \"need3\": \"Desire for international engagement\"\
#   },\
#   \"User\": \"Sports Enthusiast\"\
# }"

# x = parse_input_to_csv(str(text))
# print(x)

import json
import os
os.system('clear')
def parse_nested_input_to_csv(input_str):
    try:
        # Analisi dell'input come un dizionario
        data = json.loads(input_str)

        # Estrazione del dizionario per "Italian Local Resident"
        resident_data = data.get("Italian Local Resident", {})

        # Estrazione dei campi richiesti
        sex = resident_data.get("Sex", "")
        needs = resident_data.get("Needs", [])
        hashtags = resident_data.get("Hashtags", [])

        # Converti liste in stringhe separate da virgole
        needs_str = ';'.join(needs)
        hashtags_str = ';'.join(hashtags)

        # Creazione della stringa CSV
        csv_str = ','.join([sex, needs_str, hashtags_str])
        return csv_str

    except json.JSONDecodeError:
        # Gestisce errori di formattazione
        return "Errore di formattazione"

# Esempio di utilizzo
input_str = """
{
    "Italian Local Resident": {
        "Sex": "Male",
        "Needs": ["Parking", "Confirmation", "Guidance"],
        "Hashtags": ["#Parking", "#LocalInfo", "#Guidance"]
    }
}
"""
print(parse_nested_input_to_csv(input_str))


