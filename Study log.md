# 学习日志
## Day1
1.使用json.dump()把字典写入JSON文件，必须配合 open(..., "w", encoding="utf-8")，而且要传文件对象，不能只传字典
2.使用json.load()读回JSON文件，同样要配合 open(..., "r", encoding="utf-8")
3.json格式取值，读回来后是字典，所以和字典一致，通过key取值
4.json.dump()其中的ensure_ascii=False，它控制写入文件时中文是否被转义成 \uXXXX
5.json.dump() 写文件，json.dumps() 出字符串。带 s 的返回字符串，不带 s 的操作文件。
6.json元组存进去，读回来变成列表。
7.json.load() 读一个不存在的文件，会抛 FileNotFoundError。需要的话要自己加 try/except 或先判断 os.path.exists()


