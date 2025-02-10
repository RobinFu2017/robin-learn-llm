from openai import OpenAI

client = OpenAI()

class ResponseService():
     def __init__(self):
        pass
     
     def generate_response(self, facts, user_question):
         the_messages=[
               {"role": "user", "content": 'Based on the FACTS, give an answer to the QUESTION, with the highest level of detail possible.'+ 
                f'QUESTION: {user_question}. FACTS: {facts}'}
            ]

         print('start to ask llm again, with context.')
         print(f'the messages is {the_messages}')
         response = client.chat.completions.create(model="gpt-3.5-turbo",  messages=the_messages)

         return (response.choices[0].message.content)