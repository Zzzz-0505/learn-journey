#文件不存在/JSON 格式错误/权限错误 三种情况各写一个处理
import json

def anomaly_handling(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            res = json.load(f)
            return {"ok":True,"error":None,"content":res}
    except FileNotFoundError:
        return {"ok":False,"error":"文件不存在","content":None}
    except json.JSONDecodeError:
        return {"ok":False,"error":"JSON 格式错误","content":None}
    except PermissionError:
        return {"ok":False,"error":"权限错误","content":None}


if __name__ == "__main__":
    print(anomaly_handling("week1-basics/JSON/season.json"),end="\n")
    print(anomaly_handling("week1-basics/JSON/no_exist.json"),end="\n")
    print(anomaly_handling("week1-basics/JSON/bad.json"),end="\n")
    print(anomaly_handling("week1-basics/JSON/no_permission.json"),end="\n")
 