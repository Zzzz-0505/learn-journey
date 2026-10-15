#**题目**：写一个程序
#1. 读取 `sample.txt` 文件，统计每个单词出现的次数
#2. 输出出现频率最高的前 10 个单词（单词 + 次数）
#3. 把结果保存成 `result.json`（格式：`[{"word": "the", "count": 42}, ...]`）
#4. 如果 `sample.txt` 不存在，程序要友好提示而不是崩溃
#5. 用至少 2 个函数组织代码，并用 `if __name__ == "__main__":` 作为入口
import json
import os
from pathlib import Path

save_path = Path(__file__).parent / "result.json"

def find_word(path):
    d = {}
    result = []
    try:
        with open(path,"r",encoding="utf-8") as f:
            for line in f:          
                for word in line.split():       
                    d[word] = d.get(word,0) + 1  
        top10 = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]
        for word, count in top10:
            result.append({"word": word, "count": count})
        with open(save_path,"w",encoding="utf-8")as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        return {"ok":True,"content":"出现频率最高的前 10 个单词(单词 + 次数)已经保存到'result.json'","error":None}
    except FileNotFoundError :
        return {"ok":False,"content":None,"error":"文件不存在，请输入正确路径"}

def main():
    return find_word("Path(__file__).parent / 'sample.txt'")
    




if __name__ == "__main__":
    # res = main()
    # print(res)

#再写一个 30 行脚本：读一个 JSON 文件 → 改一个字段 → 写回去
    with open(Path(__file__).parent /"result.json","r",encoding="utf-8")as f:
        start = json.load(f)
        for item in start:
            if item.get("word") == "date":
                item["word"] = "datw"
    with open (Path(__file__).parent /"result.json","w",encoding="utf-8")as f:
        json.dump(start,f,ensure_ascii=False,indent=2)

    print("修改成功!")

    #缺少 顶层类型检查、元素类型检查