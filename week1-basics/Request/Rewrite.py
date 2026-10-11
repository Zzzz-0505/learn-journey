#主流程：取数据 → 解析 → 存文件，统一处理异常。
import json
import requests

API_URL = "https://api.open-meteo.com/v1/forecast" 
SAVE_PATH = "/Users/zzzz/Desktop/Learn-journey-git/week1-basics/weather_hangzhou.json"
OUT_TIME=10
PARAMS={

}

def fetch_data(url,params=None):
    res = requests.get(url,params=params,timeout=OUT_TIME)
    res.raise_for_status()
    r = res.json()
    return r
def fix_data(raw):
    result ={
        
    }
    return result

def save_file(file,path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(file,f,ensure_ascii=False,indent=2)


def main():
    try:
        save_file(fix_data(fetch_data(API_URL,params=PARAMS)),SAVE_PATH)
        return {}
    except:
        return {}