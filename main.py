from Utility import Utility
from gpt import GPT
from databaseService import DatabaseService
import time

# Create a GPT object
# chatGpt = GPT(engine='gpt-3.5-turbo-16k')
chatGpt = GPT(engine='gpt-3.5-turbo-16k')

other_pagesBaseUrl = 'https://www.tripadvisor.it/ShowForum-g187768-i20'  # The base url used to change pages

# The url of the first to page to crawl
first_page_url = 'https://www.tripadvisor.it/ShowForum-g187768-i20-o2580-Italy.html'

base_url = "https://www.tripadvisor.it"  # The base url of the website, used to change pages

current_page_number = 2580  # The number of the first page of the forum to crawl

forumPage = Utility.get_page(first_page_url)  # Send an HTTP GET request to the URL

# td_elements containing the td elements and inside them the posts
td_elements = forumPage.find_all('td', class_='')

# forumcol_elements containing the td elements and inside them the name of the city
forumcol_elements = forumPage.find_all('td', class_='forumcol')

enum = enumerate(td_elements)
index = next(enum)

'''This function changes the page and updates the td_elements and forumcol_elements'''


def changePage():
    global forumPage
    global current_page_number
    global td_elements
    global forumcol_elements
    global enum
    forumPage = Utility.get_page(Utility.generate_next_page_url(other_pagesBaseUrl, current_page_number))
    td_elements = forumPage.find_all('td', class_='')
    forumcol_elements = forumPage.find_all('td', class_='forumcol')
    current_page_number += 20
    enum = enumerate(td_elements)
    print("PAGE CHANGED! NUMBER: ", current_page_number)


postsToIterate = 0  # numberOfIteration is used to limit the number of posts to analyze

haltCondition = True  # This condition is used to stop the loop when the limit of posts to analyze is reached

'''Loop through the pages and posts of Tripadvisor italy forum, and for each post get the text, username, 
city of origin of the post writer, city for which the question is beeing asked then send them to chatgpt to get the 
an estimations of the needs expressed in the text of the post, then save the data in the csv file'''

while haltCondition:

    td_element = td_elements[index[0]]
    b_elements = td_element.find_all('b')

    for b_element in b_elements:  # Loop through the <b> elements, inside <b> there is the description of the post
        a_element = b_element.find('a')  # Find the <a> element, inside <a> there is the link to the post

        if postsToIterate > 20:  # Limit the number of posts to analyze
            haltCondition = False
            break

        if a_element:
            cityQuestionedInPost = Utility.getNameOfQuestionedCity(
                forumcol_elements.pop(1))  # Save the name of the city for which the question is asked

            href = a_element.get('href')  # Get the href attribute of the <a> element
            postPage = Utility.get_page(base_url + href)  # Get the page of the post

            cityOfProvenanceOfUser = Utility.getCityOfProvenanceOfUser(
                postPage)  # Save the city of provenance of the user
            usernameOfUser = Utility.getUsernameFromHtml(postPage)  # Save the name of the user

            try:
                if usernameOfUser != "Fail":
                    postText = Utility.extractPostText(postPage)  # Save the text of the post
                    chatGptPrompt = chatGpt.prompt + "Username: " + usernameOfUser + " text: " + "\" " + postText + "\""
                    print("waiting for ChatGPT response...")
                    responseFromChatGpt = chatGpt.get_response(chatGptPrompt)  # Get the response from chatgpt
                    print(responseFromChatGpt)
                    DatabaseService.save(responseFromChatGpt, cityQuestionedInPost, cityOfProvenanceOfUser)

            except Exception as e:
                print("error: ", e)
                pass

    if (td_elements.index(
            td_element) >= 37):  # If the index of the element is equal to the number of iteration then it means that
        # we are at the end of the page (each page has 20 posts, but 37 td elements)
        changePage()

    postsToIterate += 0.5
    time.sleep(1)
    index = next(enum)
