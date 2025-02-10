from openai import OpenAI
import json



client = OpenAI()


def multiplication_calculate(nunmber_a,nunmber_b):
    c = nunmber_a*nunmber_b
    print(f"{nunmber_a}*{nunmber_b}={c}")
    return c





def call_llm(use_model, prompt):
    the_msg=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    # 发起第一次调用
    response = client.chat.completions.create(
        model=use_model,
        messages=the_msg
    )
    #print(response)

    response_message = response.choices[0].message
    print("结果：")
    print(response_message.content)
    return response_message



call_llm("gpt-3.5-turbo","计算91821*81202")
call_llm("gpt-4o","计算91821*81202")