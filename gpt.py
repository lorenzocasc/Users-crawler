import openai

#original_prompt = "Generate a python dictionary containing:  birth sex (from username and text), as many user persona as you can, and associated need, with this format: Sex: Male or Female or Uncertain, Need (max 4 words): need1, need2, etc and User: user. (Examples of users can be Tourist, Student, Local, Culinary tourist, Art Tourist, Erasmus Student, etc). Also is very important that if no user or need can be precisely derivated from the text provided, you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words maximum for the user description. Answer with a python dictionary. Avoid any unecessary text or comment. If text provided includes links write SPAM. Text provided: "
api_key = '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'

original_prompt = "Generate a json object containing: sex (from username and text), user_type, and associated need, with this format: Sex: Male or Female or Uncertain, need1, need2, need3, need4, if only one or two needs can be generated write only them, also the needs must have max 4 words length, and User_type: user persona. (Examples of users can be Tourist, Student, Local, Culinary tourist, Art Tourist, Erasmus Student, etc). Also is very important that if no user or need can be precisely derivated from the text provided, you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words maximum for the user_type. Answer with a JSON Object. Avoid any unecessary text or comment. If text provided includes links write yes in field spam. There is an example of the JSON object you should provide: { \"username\" : \"username provided in text\", \"sex\" : \"guess the sex from the username and from the text\", \"need1\" : \"Guess the need1 from text\", \"need2\" : \"guess the need2 from text\", \"need3\" : \"guess the need3 from text\", \"need4\" : \"guess the need 4 from text\", \"user_type\" : \"establish a user-persona based on the informations you have\", \"spam\" : \"establish if the post is a spam post or not\" } It's important that if no needs can be established you don't write needs, also you should create user_type and need keeping in mind that similar need must be written the same way, and similar user_type must be written the same way because I will have to go and analyze them. For Example: If you write the need \"accommodation advice\" don't write in another need \"advice accommodation\" but \"accommodation advice\". The same goes for user_type. Text provided: "

class GPT:
    def __init__(self, engine):
        self.api_key = api_key
        self.engine = engine
        self.prompt = original_prompt

    def submit_request(self, modified_prompt):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant, expert of Project Design. You are a helpful assistant, expert of Project Design. You are being used to categorize a large dataset. Here is the format of the JSON you should provide me: { \"username\" : \"username provided in text\",  \"sex\" : \"guess the sex from the username and from the text\", \"need1\" : \"Guess the need1 from text\", \"need2\" : \"guess the need2 from text\", \"need3\" : \"guess the need3 from text\", \"need4\" : \"guess the need 4 from text\", \"user_type\" : \"establish a user-persona based on the informations you have\", \"spam\" : \"establish if the post is a spam post or not\" } It's important that if no needs can be established you don't write needs, also you should create user_type and need keeping in mind that similar need must be written the same way, and similar user_type must be written the same way because I will have to go and analyze them. For Example: If you write the need \"accommodation advice\" don't write in another need \"advice accommodation\" but \"accommodation advice\". The same goes for user_type. "},
                {"role": "user", "content": modified_prompt},
            ],
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message = response.choices[0]['message']
        response = "{}: {}".format(message['role'], message['content'])
        return response

    def get_response(self, modified_prompt):
        response = self.submit_request(modified_prompt)
        return response
