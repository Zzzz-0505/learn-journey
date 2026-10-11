#**HTTP + requests**：调一个公开 API（如天气或汇率），解析 JSON，存到文件
import os
import json
import requests


# 配置区：API 地址、参数、输出路径
API_URL = "https://api.open-meteo.com/v1/forecast"        
OUTPUT_PATH = "/Users/zzzz/Desktop/Learn-journey-git/week1-basics/weather_beijing.json"    # 填输出 JSON 文件路径
TIMEOUT = 10             # 请求超时秒数
params = {
    "latitude": 39.9042,
    "longitude": 116.4074,
    "current_weather": True
}

def fetch_data(url, params=None):
    """
    发 HTTP 请求，返回解析后的字典。
    步骤提示：
    1. 用 requests.get 发请求，带上 params 和 timeout
    2. 调用 raise_for_status() 检查状态码
    3. 调用 response.json() 解析 JSON
    4. 返回解析结果
    """
    # TODO: 发请求并返回解析后的数据
    res = requests.get(url,params=params,timeout=TIMEOUT)
    res.raise_for_status()
    data = res.json()
    return data 


def parse_data(raw):
    """
    从原始响应里提取需要的字段，返回整理后的字典。
    步骤提示：
    1. 确认 raw 的结构，是字典还是列表
    2. 按 key 逐层取值，必要时用 get() 避免 KeyError
    3. 只保留你关心的字段，组成新字典
    4. 返回新字典
    """
    # TODO: 提取字段并返回整理后的结果
    result={
        "latitude":raw['latitude'],
        "longitude":raw['longitude'],
        "time":raw['current_weather']['time'],
        "temperature":raw['current_weather']['temperature']
    }
    return result


def save_json(data, path):
    """
    把字典写入 JSON 文件。
    步骤提示：
    1. 确认目标目录存在，不存在就创建
    2. 用 with open(..., "w", encoding="utf-8") 打开文件
    3. 用 json.dump 写入，设 ensure_ascii=False 和 indent
    """
    # TODO: 写入 JSON 文件
    with open(path,"w",encoding="utf-8") as f:    
        json.dump(data, f,ensure_ascii=False,indent=2)




def main():
    """
    主流程：取数据 → 解析 → 存文件，统一处理异常。
    异常处理提示：
    - requests.exceptions.Timeout：请求超时
    - requests.exceptions.ConnectionError：网络不通
    - requests.exceptions.HTTPError：4xx/5xx
    - json.JSONDecodeError：响应不是合法 JSON
    - KeyError：取字段时 key 不存在
    - OSError：写文件失败
    - 最后用 requests.exceptions.RequestException 兜底
    """
    # TODO: 调用 fetch_data、parse_data、save_json
    # TODO: 用 try/except 包裹，分别处理上面列出的异常
    try:
        raw = fetch_data(API_URL,params=params)
        save_json(parse_data(raw),OUTPUT_PATH)
        return {"ok": True, "message": "获取成功"}
    except requests.exceptions.Timeout:
        return {"ok": False, "message":"请求超时"}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "message":"网络不通"}
    except requests.exceptions.HTTPError:
        return {"ok": False, "message":"4xx/5xx"}
    except json.JSONDecodeError:
        return {"ok": False, "message":"响应不是合法 JSON"}
    except KeyError:
        return {"ok": False, "message":"key 不存在"}
    except OSError:
        return {"ok": False, "message":"写文件失败"}
    except requests.exceptions.RequestException:
        return {"ok": False, "message":"存在错误"}



if __name__ == "__main__":
    res = main()
    print(res)