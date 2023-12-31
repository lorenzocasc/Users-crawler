from bs4 import BeautifulSoup
import requests
import random


#headers = {
#    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
#                  'Chrome/98.0.4758.102 Safari/537.36'
#}


headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.8,image/webp,*/*;q=0.7',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.7,fr;q=0.3',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-store',
        'Pragma': 'no-cache',
        'TE': 'Trailers'
    }
]


'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.8,image/webp,*/*;q=0.7',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.7,fr;q=0.3',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-store',
    'Pragma': 'no-cache',
    'TE': 'Trailers'
}
'''


"""
This function reformats the text of the post.

Parameters:
text_list (List): List of the text of the post.

Returns:
String: The text of the post.
"""


def format_postText(text_list):
    text = ''
    for elem in text_list:
        text += elem.replace('"', '') + ' '
    text = text.replace(',', '')
    text = text.replace("", '')
    return text


class Utility:
    def __init__(self):
        pass

    """
    This function search for the element 'div' with class 'username' 
    to save the username of the user who posted the comment..

    Parameters:
    postHtml (Object): Html of the post.

    Returns:
    String: The username of the user who made the post.
    """

    @staticmethod
    def getUsernameFromHtml(postHtml):

        username_element = postHtml.find('div', class_='username')
        if username_element is not None:
            username = username_element.find('a')
        try:
            if username:
                username = username.text.strip()
                return username if username != "Matteo Z" else "Fail"
        except Exception as e:
            print("error in getUsernameFromHtml function in Utily class: ", e)
            return "Impossibile to get the username"

    """
    This function search for the element 'div' with class 'location'
    to save the city of provenance of the user who posted the comment..
    
    Parameters:
    postPage (Object): Html of the post.
    
    Returns:
    String: The city of provenance of the user who made the post.
    """

    @staticmethod
    def getCityOfProvenanceOfUser(postPage):
        cityOfProvenance_element = postPage.find('div', class_='location')
        if cityOfProvenance_element:
            cityOfProvenance = cityOfProvenance_element.text.strip()
            return cityOfProvenance

    """
    This function does a request to the url passed as parameter and returns the html of the page.
    
    Parameters:
    url (String): Url of the web-page.
    
    Returns:
    String: html of the page (Object).
    """

    @staticmethod
    def get_page(url):
        headers = random.choice(headers_list)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print("Failed to retrieve the webpage. Status code: {}", response.status_code)
            return None

    """
    This function search for the element 'div' with class 'postBody'
    to save the text of the post.
    
    Parameters:
    postPage (Object): Html of the post.
    
    Returns:
    String: The text of the post.
    """

    @staticmethod
    def extractPostText(postPage):
        post_text = []
        htmlPostBody_elements = postPage.find_all('div', class_='postBody')

        for htmlPostBody_element in htmlPostBody_elements:
            p_elements = htmlPostBody_element.find_all('p')
            for p_element in p_elements:
                post_text.append(p_element.text.strip())
            break  # Stopping after extracting the text of the post, otherwise
            # it will extract also the text of the comments

        postFormattedText = format_postText(post_text)
        return postFormattedText

    """
    This calculates the next page number and generates the URL for the next page
    with this method 
    
    Parameters:
    url (String): Url of actual web-page.
    
    Returns:
    String: The url of the next page.
    """

    @staticmethod
    def generate_next_page_url(url, page, items_per_page=20):
        # Calculate the next page number
        next_page_number = page + items_per_page

        # Generate the URL for the next page
        next_page_url = f"{url}-o{next_page_number}-Italy.html"

        return next_page_url

    """
    This function saves the name of the city for which the post is being made
    Example: I'm going to Rome tomorrow, what should I visit? -> Rome
    
    Parameters:
    forumcol_element (Object): Html of the post.
    
    Returns:
    String: The name of the city.
    """

    @staticmethod
    def getNameOfQuestionedCity(forumcol_element):

        city_element = forumcol_element.find('a')
        if city_element:
            city = city_element.text.strip()
            return city
