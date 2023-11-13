import time
import requests
import ast
from bs4 import BeautifulSoup
from gpt import GPT
from databaseService import DatabaseService
import csv
import os
import re
import json


os.system('clear')

csv_filename = "output_crawler.csv"

# Open the file in write mode ('w') and create a csv.writer object
# with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#     csvfile.write('city_topic,city_origin,username,sex,user_personas,needs\n')

# Set your openai API key
api_key = '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'

# Create a GPT object
# chatGpt = GPT(api_key=api_key, engine='gpt-3.5-turbo-16k')
chatGpt = GPT(api_key=api_key, engine='gpt-4')

# Chatgpt prompt to be used
# prompt = ("Generate birth sex(from username), user type and associated need, with this format: Sex: [Male] or ["
#           "Female] or Uncertain, Need: [need1] (description of need) 2), [need2] (description of need), "
#           "etc and User: [user]. (Examples of users can be Tourist, Student, Local, etc)"
#           "Also is very important that if no user or need can be precisely derivated from the text provided, "
#           "you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words "
#           "maximum for the user description. Answer with a single sentence . Text provided:")

promptx = "I'm providing you username and text of a post, from these two you have to determine the sex, the needs and the user persona. Its important that the user persona isn't so specific. Also if no needs or user persona can be determined you should simply return \"impossibile\". If no sex can be established you have to return \"undefined\". Provide the data i requested in a python dictionary with no more addition. Here is the text provided: "
promptt = "Fornito username e un testo associato, determina il sesso e i 'bisogni' dell'utente. E' importante che i bisogni non siano troppo specifici. Se non riesci a determinare i bisogni o il tipo di utente, scrivi semplicemente \"impossibile\". Se non riesci a determinare il sesso, scrivi \"undefined\". Fornisci i dati richiesti in un dizionario python senza ulteriori aggiunte. Ecco il testo fornito: "
prompt = "Generate a python dictionary containing:  birth sex (from username and text), as many user persona as you can, and associated need, with this format: Sex: Male or Female or Uncertain, Need (max 4 words): need1, need2, etc and User: user. (Examples of users can be Tourist, Student, Local, Culinary tourist, Art Tourist, Erasmus Student, etc). Also is very important that if no user or need can be precisely derivated from the text provided, you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words maximum for the user description. Answer with a python dictionary. Avoid any unecessary text or comment. If text provided includes links write SPAM. Text provided: "
# prompt = "Create a Python dictionary from the text provided. Identify as many user persona as you can from analysing the text, give them a meaningful not so specific name based on what you think it is and use it as a key. For each key, include a nested dictionary with 'Sex', 'Needs and 'Hashtags' attributes. The 'Sex' should be assigned as 'Male', 'Female', or 'Uncertain' based on the text, and 'Needs' should be a list of needs directly inferred from the text of 3 words max. The Hashtags should be a list of one word only hashtags relevant to that user persona, so that after we can do clustering of these persona even if they are named different. Detect the spam messages. Spam messages should be the one with URLs or spamming things (so no requests found in the text). If you detect a Spam message responde just SPAM. Provide only the dictionary. Here is the text provided:"
# prompt = "Generate a python dictionary containing: birth sex (from username and text), as many user persona as you can, and associated need, with this format: Sex: Male or Female or Uncertain, Need: need1 (description of need1), need2 (description of need2), etc and User: user. (Examples of users can be Tourist, Student, Local, Culinary tourist, Art Tourist, Erasmus Student, etc). Also is very important that if no user or need can be precisely derivated from the text provided, you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words maximum for the user description. Answer with a python dictionary. Avoid any unecessary text or comment. If text provided includes links write SPAM. Here is a series of examples of the text provided and the output expected: EXAMPLE1 Text provided: Username: ATOMICJOE, Text: Buongiorno a tutti , volevo consigli per un villaggio in Calabria sul mare che abbia animazione . Ho una ragazza di 16 anni e ovviamente per lei sarebbe fondamentale !! Grazie in anticipo !! n.b. 10 gg ad Agosto. Response expected: { \"Sex\": \"Undefined\", \"User\": \"Tourist\", \"Spam\": \"No\", \"Needs\": { \"Need1\" : \"Advice for seaside village in Calabria\", \"Need2\" : \"Animation for kids\" } } EXAMPLE2 Text provided: Username: Simone C, Text: Buongiorno, siamo una coppia in cerca di relax e belle spiagge. Palesemente coscienti del periodo d'alta stagione cerchiamo consiglio su zone meno affollate. Cercando di qua e di là ho notato che la parte sud-occidentale della Sardegna è la più vivibile in quel periodo. Noi atterreremo a Cagliari, dove noleggeremo una macchina. Staremo dal 10 al 17 di Agosto (obbligati dal lavoro). Mi hanno consigliato Pula come meta fissa dove poi spostarci per le spiagge. La mia preoccupazione è che sia troppo caotica in quel periodo. Magari anche paesi vicini meno blasonati. Oppure costa Iglesiana con Iglesias o posti limitrofi come riferimento. Altrimenti la Costa Verde con Oristano o Cabras/paesi limitrofi. Infine, cosa più importante, in quale di queste zone le spiagge sono meno affollate? Response expected: { \"Sex\" : \"Male\", \"User\" : \"Tourist with partner\", \"Spam\" : \"No\", \"Needs\" : { \"need1\" : \"Advice for quite beach locations during high season\", \"need2\" : \"Car rental service in Cagliari\", \"need3\" : \"Information on less crowded tourist destinations in Southwestern Sardinia.\" } } EXAMPLE3 Text provided: Username: Glitterina, Text: Ciao a tutti, come forse saprete già, dal 1 ottobre 2023 cambiano le tariffe GTT per bigletti mezzi pubblici e pubblica sosta. Punto importante, a mio avviso, che vi segnalo: I titoli di viaggio acquistati sino al 30 settembre saranno utilizzabili dai clienti sino al 30 ottobre 2023, data dalla quale tali titoli saranno automaticamente rifiutati dai validatori GTT. I clienti che al 30 ottobre dovessero essere in possesso di titoli di viaggio con tariffa “vecchia” e non ancora usati potranno sostituirli con titoli “nuovi” (pagando la differenza) recandosi presso un Centro Servizi al Cliente di GTT, a partire dal 31 ottobre, solo su appuntamento e mediante prenotazione mediante l’applicazione Ufirst. Per tutte le nuove tariffe e specifiche, ecco il link ufficiale: https://www.gtt.to.it/cms/avvisi-e-informazioni-di-servizio ciau a tutti. Response expected { \"Spam\" : \"Yes\" } Now here is the text: "

# Chatgpt response
gptResponse = []

# Text passed to chatgpt
requestText = []

user_object = {"Username": "", "In_visit_to": "", "In_visit_from": "", "chatGptResponse": "", "prompt": "", "sex": "",
               "needs": "", "user_type": ""}

list_of_user_objects = []


# save the name of the user
def save_name(postPage):
    username_element = postPage.find('div', class_='username')
    if username_element == None:
        return
    username = username_element.find('a')
    if username:
        username = username.text.strip()
        requestText.append(
            # "Username: " +
              username
            #   + "\n"
              )
        user_object["Username"] = username
        # print("Username:", username)


# Save the city of provenance of the user
def saveCityOfProvenance(postPage):
    cityOfProvenance_element = postPage.find('div', class_='location')
    if cityOfProvenance_element:
        cityOfProvenance = cityOfProvenance_element.text.strip()
        requestText.append(
            # "City of provenience: " + 
            cityOfProvenance
            # + "\n"
            )
        user_object["In_visit_from"] = cityOfProvenance
        # print("City of Provenance: ", cityOfProvenance)


# Http request to get the page and return the html
def get_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


def loopAndSavePost(postPage):
    postText = []
    post_body_elements = postPage.find_all('div', class_='postBody')
    for post_body_element in post_body_elements:
        p_elements = post_body_element.find_all('p')
        for p_element in p_elements:
            postText.append(p_element.text.strip())
        break  # So no comments w=qill be added to the post text
    # postText.append("---- new post text ---- \n")
    for text in postText:
        requestText.append(text)
    postText.clear()


# Save the name of the city for which the question is asked
def saveNameOfTheCity(forumcol_element):
    city_element = forumcol_element.find('a')
    if city_element:
        city = city_element.text.strip()
        # print("City of Request:", city)
        user_object["In_`visit_to"] = city
        requestText.append(
            # "City of request is: " + 
            city
            # + "\n"
            )


def generate_next_page_url(url, page, items_per_page=20):
    # Calculate the next page number
    next_page_number = page + items_per_page
    # Generate the URL for the next page
    next_page_url = f"{url}-o{next_page_number}-Italy.html"
    return next_page_url

def write_row(my_string):
    # The name of the CSV file where the string will be written
    csv_filename = "output_crawler.csv"

    # Open the file in write mode ('w') and create a csv.writer object
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        # csvwriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,escapechar='\\')
        # csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvfile.write(my_string + '\n')


        # Write the string as a single row in the CSV file
        # csvwriter.writerow([my_string])

def parse_input_to_csv(input_str):
    print("Current string: \n"+input_str)
    try:
        # Analisi dell'input come un dizionario
        data = json.loads(input_str)

        # Controlla se il campo SPAM è falso o simile
        spam = data.get('spam', '')
        if isinstance(spam, bool):
            if(spam):
                print("spam")
                return "spam"
        try:
          if 'true' in spam or 'http' in spam or 'yes' in spam:
              print("spam")
              return "spam"
        except Exception as e:
            print("error: ",e)
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


        # print("user_values",user_values)
        # print("need_values",need_values)
        
        # Creazione della stringa CSV
        csv_str = ','.join([sex] + user_values + need_values)
        # sex_persona_needs = [sex,user_values,need_values]
        return csv_str
    
    except json.JSONDecodeError:
        # Gestisce errori di formattazione
        return "Errore di formattazione"

def parse_nested_input_to_csv(input_str):
    print("Current string: \n"+input_str)
    try:
        # Analisi dell'input come un dizionario
        data = json.loads(input_str)

        # Estrazione delle chiavi principali (es. "Italian Local Resident")
        main_keys = list(data.keys())

        # Preparazione della lista per i dati CSV
        csv_data = []

        for key in main_keys:
            sub_data = data[key]

            # Aggiunta della chiave principale (es. tipo di utente)
            csv_data.append(key)

            # Iterazione su ogni sottochiave e raccolta dei valori
            for sub_key, value in sub_data.items():
                if isinstance(value, list):
                    # Unisce gli elementi della lista con ';'
                    csv_data.append(';'.join(value))
                else:
                    # Aggiunge direttamente il valore se non è una lista
                    csv_data.append(value)

        # Creazione della stringa CSV
        csv_str = ','.join(csv_data)
        return csv_str

    except json.JSONDecodeError:
        # Gestisce errori di formattazione
        return "Errore di formattazione"


# URL of the webpage you want to crawl
other_pagesBaseUrl = 'https://www.tripadvisor.it/ShowForum-g187768-i20'
first_page_url = 'https://www.tripadvisor.it/ShowForum-g187768-i20-o1440-Italy.html'
#first_page_url = 'https://www.tripadvisor.it/ShowForum-g187768-i20-o20300-Italy.html'
base_url = "https://www.tripadvisor.it"

current_page_number = 1440

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36'
}

# Send an HTTP GET request to the URL
forumPage = get_page(first_page_url)

# td_elements containing the td elements and inside them the posts
td_elements = forumPage.find_all('td', class_='')

# forumcol_elements containing the td elements and inside them the name of the city
forumcol_elements = forumPage.find_all('td', class_='forumcol')

# numberOfIteration is used to limit the number of posts to analyze
numberOfIteration = 0  # Number of iteration to do

# Loop through the <td> elements to find the one with the link you want
# for index in enumerate(td_elements):  # Loop through the <td> elements, almost each element is a post

haltCondition = True
enum = enumerate(td_elements)
index = next(enum)
while haltCondition:
    td_element = td_elements[index[0]]
    b_elements = td_element.find_all('b')
    for b_element in b_elements:  # Loop through the <b> elements, inside <b> there is the description of the post
        a_element = b_element.find('a')  # Find the <a> element, inside <a> there is the link to the post

        if numberOfIteration > 1000:  # Limit the number of iteration, each element needs 2 iteration
            haltCondition = False
            break

        if a_element:
            saveNameOfTheCity(forumcol_elements.pop(1))  #Save the name of the city of the post
            href = a_element.get('href')  #Get the href attribute of the <a> element
            postPage = get_page(base_url + href)  #Get the page of the post
            saveCityOfProvenance(postPage)
            save_name(postPage)
            try:
              if user_object["Username"] != "Matteo Z":
                loopAndSavePost(postPage)  #Loop through the post and save the text
                user_object["prompt"] = prompt + "\n" + str(requestText)  #Save the prompt used for chatgpt in user_object
                print("waiting for ChatGPT response...")
                response = chatGpt.get_response(prompt + "\n" + str(requestText))  #Get the response from chatgpt
                print(response)
                gptResponse.append(response)  #Save the response in gptResponse array
                user_object["chatGptResponse"] = response  #Save the response in user_object
                user_object["sex"] = "Unknown"
                user_object["needs"] = "Unknown"
                user_object["user_type"] = "Unknown"
                list_of_user_objects.append(user_object.copy())  # Save the user_object in the list of user objects
                user_object.clear()  # Clear the user_object
              else:
                print("SKIPPO Matteo Z")

            except Exception as e:
                print("error: ",e)
                pass


    print("td_elements.index(td_element) ",td_elements.index(td_element))
    print("current_page_number ",current_page_number)
    if (td_elements.index(td_element) >= 37):  # If the index of the element is equal to the number of iteration then it means that
        # we are at the end of the page
        forumPage = get_page(generate_next_page_url(other_pagesBaseUrl, current_page_number))
        td_elements = forumPage.find_all('td', class_='')
        forumcol_elements = forumPage.find_all('td', class_='forumcol')
        current_page_number += 20
        enum = enumerate(td_elements)
        print("PAGE CHANGED! NUMBER: ", current_page_number)

    if numberOfIteration % 2 != 0:
        if len(requestText) > 3:
            city_request = requestText[0].replace('"', '')
            city_provenance = requestText[1].replace('"', '')
            city_provenance = requestText[1].replace(',', '')
            username = requestText[2].replace('"', '')
            #from now on, requests' lines
            post_text = ''
            for elem in requestText[3:]:
                post_text += elem.replace('"', '') + ' '
            post_text = post_text.replace(',', '')
            post_text = post_text.replace('"', '')
            post_text = '"'+post_text+'"'
            # print("post_text: ",post_text)

            final_row = city_request+','+city_provenance+','+username+','
            final_row_post_text = final_row + post_text
            # response = chatGpt.get_response(prompt + "\n" + "Username: " + username + " text: " + post_text)  # Get the response from chatgpt
            final_row_response = final_row + "," + str(response)

            
            clean_string = str(response)[11:]
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

    requestText.clear()
    user_object.clear()
    numberOfIteration += 1
    time.sleep(1)
    index = next(enum)


# db = DatabaseService(list_of_user_objects)
# db.extend()
# #db.print()

# db.save()

#%%
