from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  #model="gpt-4o",
  model="gpt-4",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "武汉意大利热干面是什么"
        }
      ]
    }
  ],
  temperature=1.1,
  max_tokens=512,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


print(response.choices[0].message)