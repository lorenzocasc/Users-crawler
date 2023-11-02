import openai

class GPT:
    def __init__(self, api_key, engine='gpt-3.5-turbo'):
        self.api_key = api_key
        self.engine = engine

    def submit_request(self, prompt):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant, expert of Project Design."},
                {"role": "user", "content": prompt},
            ])
        message = response.choices[0]['message']
        response = "{}: {}".format(message['role'], message['content'])
        return response

    def get_response(self, prompt):
        response = self.submit_request(prompt)
        return response
