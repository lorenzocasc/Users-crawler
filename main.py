import requests
from bs4 import BeautifulSoup
from gpt import GPT

# Set your openai API key
api_key = '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'

# Create a GPT object
chatGpt = GPT(api_key=api_key, engine='gpt-3.5-turbo')

# Chatgpt prompt to be used
prompt = ("Generate birth sex(from username), user type and associated need, with this format: Sex: [Male] or ["
          "Female] or [Uncertain], Need: [need1] (description of need) 2) [need2] (description of need), "
          "etc and User: 1) [user1]. (Like Tourist, Student, Local, etc)"
          "Also is very important that if no user or need can be precisely derivated from the text provided, "
          "you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words "
          "maximum for the user description. Text provided:")

# Chatgpt response
gptResponse = []

# Text passed to chatgpt
requestText = []

# save the name of the user
def save_name(postPage):
    username_element = postPage.find('div', class_='username')
    username = username_element.find('a')
    if username:
        username = username.text.strip()
        requestText.append("The username is: " + username)
        print("Username:", username)


# Save the city of provenance of the user
def saveCityOfProvenance(postPage):
    cityOfProvenance_element = postPage.find('div', class_='location')
    if cityOfProvenance_element:
        cityOfProvenance = cityOfProvenance_element.text.strip()
        requestText.append("The city of provenience is: " + cityOfProvenance)
        print("City of Provenance:", cityOfProvenance)

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
        break #So no comments will be added to the post text
    gptResponse = chatGpt.get_response(prompt + str(postText))
    print("GPT Response:", gptResponse)
    postText.append("---- new post text ---- \n")
    for text in postText:
        requestText.append(text)
    postText.clear()


# Save the name of the city for which the question is asked
def saveNameOfTheCity(forumcol_element):
    city_element = forumcol_element.find('a')
    if city_element:
        city = city_element.text.strip()
        print("City of Request:", city)
        requestText.append("The city of request is: " + city)


# URL of the webpage you want to crawl
url = 'https://www.tripadvisor.it/ShowForum-g187768-i20-Italy.html'
base_url = "https://www.tripadvisor.it"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36'
}

# Send an HTTP GET request to the URL
forumPage = get_page(url)

# td_elements containing the td elements and inside them the posts
td_elements = forumPage.find_all('td', class_='')

# forumcol_elements containing the td elements and inside them the name of the city
forumcol_elements = forumPage.find_all('td', class_='forumcol')

# numberOfIteration is used to limit the number of posts to analyze
numberOfIteration = 0  # Number of iteration to do

# Loop through the <td> elements to find the one with the link you want
for td_element in td_elements:  # Loop through the <td> elements, almost each element is a post
    b_elements = td_element.find_all('b')
    if (numberOfIteration == 5):
        break
    numberOfIteration += 1
    for b_element in b_elements:  # Loop through the <b> elements, inside <b> there is the description of the post
        a_element = b_element.find('a')  # Find the <a> element, inside <a> there is the link to the post
        requestText.append("////////////////")
        if a_element:
            saveNameOfTheCity(forumcol_elements.pop(1))  # Save the name of the city of the post
            href = a_element.get('href')  # Get the href attribute of the <a> element
            postPage = get_page(base_url + href)  # Get the page of the post
            saveCityOfProvenance(postPage)
            save_name(postPage)
            loopAndSavePost(postPage)  # Loop through the post and save the text



print("Request Text:", requestText)
