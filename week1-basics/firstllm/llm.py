import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("/Users/zzzz/Desktop/Learn-journey-git/.env")

PATH="/Users/zzzz/Desktop/Learn-journey-git/week1-basics/firstllm/chat-history.json"

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""
if os.path.exists(PATH):
    with open(PATH, "r", encoding="utf-8") as f:
        history_list = json.load(f)

    if not isinstance(history_list, list):
        history_list = []
else:
     history_list = []

if not history_list or history_list[0].get("role") != "system":
    history_list.insert(0, {"role": "system", "content": system_prompt})


while True:
    print("请输入你的问题:(以输入exit结束对话)")
    input_content = input()

    if input_content != "exit":
        history_list.append({
            "role": "user", 
            "content": input_content
            })
        
        messages = history_list

        response = client.chat.completions.create(
                    model="deepseek-flash",
                    messages=messages,
                    response_format={"type": "json_object"}
                    )
        history_list.append({
                "role": "assistant",
                "content": response.choices[0].message.content
                })
        
        print(json.loads(response.choices[0].message.content))

        with open(PATH,'w',encoding="utf-8") as f:
            json.dump(history_list,f,ensure_ascii=False,indent=2)
        
    else:
        print("对话结束！对话历史已经保存在'chat-history.json'文件里")
        break

