import openai

original_prompt = "Generate a python dictionary containing:  birth sex (from username and text), as many user persona as you can, and associated need, with this format: Sex: Male or Female or Uncertain, Need (max 4 words): need1, need2, etc and User: user. (Examples of users can be Tourist, Student, Local, Culinary tourist, Art Tourist, Erasmus Student, etc). Also is very important that if no user or need can be precisely derivated from the text provided, you should write me \"Impossibile\". I need short-medium sentences for needs. One, two or three words maximum for the user description. Answer with a python dictionary. Avoid any unecessary text or comment. If text provided includes links write SPAM. Text provided: "
api_key = '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'


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
                {"role": "system", "content": "You are a helpful assistant, expert of Project Design."},
                {"role": "user", "content": modified_prompt},
            ],
            temperature=1,
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
