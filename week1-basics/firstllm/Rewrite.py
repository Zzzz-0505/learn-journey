# Please install OpenAI SDK first: `pip3 install openai`
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("/Users/zzzz/Desktop/Learn-journey-git/.env")
PATH="/Users/zzzz/Desktop/Learn-journey-git/week1-basics/firstllm/chat-history2.json"

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

system_prompt="""
        You are useful assistant,you can help user work everything,
        when user offer a question,please respond use JSON formal.
        For example:
        {
        "user":"which is the longest river in the world?",
        "assistant":"Nile river"
        }

"""
if os.path.exists(PATH):
    with open(PATH,"r",encoding="utf-8") as f:
        history_list = json.load(f) 
    if not isinstance(history_list,list):
        history_list =[]
else:
    history_list =[]

if not history_list or history_list[0].get("role") != "system":
    history_list.insert(0,{"role": "system", "content": system_prompt})

while True:
    print("请输入你的问题:(以exit结束对话)")
    content=input()

    if content != "exit":
        message_user ={"role":"user","content":content}
        history_list.append(message_user)

        messages = history_list
        response = client.chat.completions.create(
                model="deepseek-flash",
                messages=messages,
               response_format={ "type": "json_object"}
        )  
        print(response.choices[0].message.content)

        message_llm ={"role":"assistant","content":response.choices[0].message.content}
        history_list.append(message_llm)

        with open(PATH,"w",encoding="utf-8") as f:
            json.dump(history_list,f,ensure_ascii=False,indent=2)
    else:
        print("对话结束！对话历史已经保存在'chat-history2.json'文件里")
        break