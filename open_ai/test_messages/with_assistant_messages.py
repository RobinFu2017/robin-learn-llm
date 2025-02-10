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
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "武汉并没有意大利热干面"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "那武汉意大利热干面到底是什么"
        }
      ]
    },
  ],
  temperature=1.1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


print(response.choices[0].message)