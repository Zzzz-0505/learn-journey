#**题目**：写一个程序
#1. 读取 `sample.txt` 文件，统计每个单词出现的次数
#2. 输出出现频率最高的前 10 个单词（单词 + 次数）
#3. 把结果保存成 `result.json`（格式：`[{"word": "the", "count": 42}, ...]`）
#4. 如果 `sample.txt` 不存在，程序要友好提示而不是崩溃
#5. 用至少 2 个函数组织代码，并用 `if __name__ == "__main__":` 作为入口
import json,shutil
from pathlib import Path

def find_top10(word_path,save_path):
    d={}
    result=[]
    try:
        with open(word_path,"r",encoding="utf-8")as f:
            for line in f:
                for word in line.split():
                    d[word] = d.get(word,0)+1
        top10 = sorted(d.items(),key=lambda x:x[1],reverse=True)[:10]
        for word,count in top10:
            result.append({"word":word,"count":count})
        with open(save_path,"w",encoding="utf-8")as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        return "ok"
    except FileNotFoundError:
        return "error"
def main():
    word_path = Path(__file__).parent / "sample.txt"
    save_path = Path(__file__).parent / "result.json"
    return find_top10(word_path=word_path,save_path=save_path)

def change_data():
    path = Path(__file__).parent.resolve()/ "result.json"
    shutil.copy(path,path.with_suffix(".json.bak"))

    with open(path,"r",encoding="utf-8")as f:
        text = json.load(f)
        count = 0
        if not isinstance(text,list):
            return f"TypeError,类型不匹配"
        for item in text:
            if isinstance(item,dict) and  item.get("word") == "for":
                item["word"] = "forrrrr"
                count += 1
    with open(path,"w",encoding="utf-8")as f:
        json.dump(text,f,ensure_ascii=False,indent=2)
    return f"修改成功！共修改{count}处"

if __name__ == "__main__":
    res = main()
    # print(res)
    print(change_data())