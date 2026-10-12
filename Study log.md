# 学习日志
## Day1
1.使用json.dump()把字典写入JSON文件，必须配合 open(..., "w", encoding="utf-8")，而且要传文件对象，不能只传字典
2.使用json.load()读回JSON文件，同样要配合 open(..., "r", encoding="utf-8")
3.json格式取值，读回来后是字典，所以和字典一致，通过key取值
4.json.dump()其中的ensure_ascii=False，它控制写入文件时中文是否被转义成 \uXXXX
5.json.dump() 写文件，json.dumps() 出字符串。带 s 的返回字符串，不带 s 的操作文件。
6.json元组存进去，读回来变成列表。
7.json.load() 读一个不存在的文件，会抛 FileNotFoundError。需要的话要自己加 try/except 或先判断 os.path.exists()

## Day2
1.在异常处理时，把try里正确路径的return也放在try里，这样就不依赖变量了
2.在print和return等需要参数等函数里，直接将表达式写入，使代码更简洁
3.修改文件权限可以使用chmod XXX 文件名的方式，常见的有 644 000
4.except顺序存在父类和子类，如果父类在前面，后面的子类永远不会执行
5.在文件处理时，如果没有使用 with open的话，就需要在异常处理最后加入finally，补充f.close()
6.常见的异常类：
    异常	                        触发场景
    ValueError	                值不合法，如 int("abc")
    TypeError	                类型不对，如 "a" + 1
    KeyError	                字典键不存在
    IndexError	                列表索引越界
    FileNotFoundError	        文件不存在
    PermissionError	            权限不足
    IsADirectoryError	        把目录当文件
    json.JSONDecodeError	    JSON 格式错误
    UnicodeDecodeError	        编码错误
    ZeroDivisionError	        除以零
    AttributeError	            对象没有该属性
    OSError	                    更宽泛的 I/O 错误
    Exception	                常规异常的父类，兜底
7.request可以通过在python里改变headers，把User-Agent伪装成浏览器，去访问禁止爬虫的网站
8.通过requests.get()方法获取网站信息，直接打印是状态码，通过.json()获取字典格式，用于处理数据
9.raise_for_status()是在get的过程中，如果不分析状态码，当418时也会是输出成功，只是没内容，不会抛出异常
10.处理数据的时候，需要通过print(type)去查看类型，如果是字典再分析通过键值和自己构建一个新字典，去保留需要的信息
11.函数返回信息的格式最好统一化，便于维护

## Day3
1.异步的价值在于并发，真正省的是在等待期间，程序可以去处理其他事情
2.异步使用场景一般有：高并发 I/O 场景、需要同时处理多件事、Web 框架 / 服务器、前端 / UI 编程
3.异步也会使代码更复杂；需要异步库；调试更难；计算密集用异步没用，需要上多线程
4.在调用大模型时，一定要控制system prompt，不然会让结果失控，无法达到预期效果
5.json文本返回到python是一种list（dict）格式，所以在增加内容时，要确保是一个list
6.json文件无法实现追加，需要将追加转换为:提取，添加再重写
7.在调用大模型API时可以参考官方API文档，通过那些示例代码可以更好上手
8.在设计程序时要考虑会出现的异常，需要考虑异常处理