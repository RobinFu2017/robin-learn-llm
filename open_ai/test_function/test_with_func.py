from openai import OpenAI
import json



client = OpenAI()


# 定义一个乘法函数
def multiplication_calculate(nunmber_a,nunmber_b):
    c = nunmber_a*nunmber_b
    print(f"{nunmber_a}*{nunmber_b}={c}")
    return c


# 用json描述这个乘法函数，后面用来告诉模型有这么一个函数可以调用
the_tools=[
    {
        "type": "function",
        "function":{
            "name": "multiplication_calculate",
            "description": "计算两个整数的乘法",
            "parameters": {
                "type": "object",
                "properties": {
                    "nunmber_a": {
                        "type": "integer",
                        "description": "The first number for calculate"
                    },
                    "nunmber_b": {
                        "type": "integer",
                        "description": "The second number for calculate"
                    }
                }
            }
        }
    }
]

# 主方法入口
def call_llm_with_function(use_model, prompt):
    # 最初的输入消息
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
        messages=the_msg,
        tools=the_tools,
        tool_choice="auto"
    )

    print(f"第一次调用结果：{response}")

    response_message = response.choices[0].message
    #print(response_message)
    # 模型返回结果里，会有方法调用的内容
    tool_calls = response_message.tool_calls
    #print(response.choices[0].message.tool_calls)

    # 处理模型让我们调用方法（帮模型调用方法，再把实际的返回值传入，第二次调用模型）
    if tool_calls:
        #
        available_functions = {
            "multiplication_calculate": multiplication_calculate,
        }
        the_msg.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            # 根据方法名，找到这个python方法
            function_to_call = available_functions[function_name]
            # 读取方法入参
            function_args = json.loads(tool_call.function.arguments)
            # 调用上面定义的python方法
            function_response = function_to_call(
                nunmber_a = function_args.get("nunmber_a"),
                nunmber_b = function_args.get("nunmber_b")
            )
            # 把python方法返回值，放入msg里面，等会调用模型用
            the_msg.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )  
        

        print(f"第二次调用的输入：{the_msg}")
        # 第二次调用模型
        second_response = client.chat.completions.create(
            model=use_model,
            messages=the_msg
        )
        print("结果：")
        print(second_response.choices[0].message.content)
        return second_response



call_llm_with_function("gpt-3.5-turbo","计算91821*81202")
#call_llm_with_function("gpt-4o","计算91821*81202")