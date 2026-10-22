# 学习日志
## Day1
1.使用json.dump()把字典写入JSON文件，必须配合 open(..., "w", encoding="utf-8")，而且要传文件对象，不能只传字典


2.使用json.load()读回JSON文件，同样要配合 open(..., "r", encoding="utf-8")


3.json格式取值，读回来后是字典，所以和字典一致，通过key取值


4.json.dump()其中的ensure_ascii=False，它控制写入文件时中文是否被转义成 \uXXX


5.json.dump() 写文件，json.dumps() 出字符串。带 s 的返回字符串，不带 s 的操作文件。


6.json元组存进去，读回来变成列表。


7.json.load() 读一个不存在的文件，会抛 FileNotFoundError。需要的话要自己加 try/except 或先判断 os.path.exists()

---

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
    PermissionError	                权限不足
    IsADirectoryError	        把目录当文件
    json.JSONDecodeError	        JSON 格式错误
    UnicodeDecodeError	        编码错误
    ZeroDivisionError	        除以零
    AttributeError	                对象没有该属性
    OSError	                        更宽泛的 I/O 错误
    Exception	                常规异常的父类，兜底
7.request可以通过在python里改变headers，把User-Agent伪装成浏览器，去访问禁止爬虫的网站


8.通过requests.get()方法获取网站信息，直接打印是状态码，通过.json()获取字典格式，用于处理数据


9.raise_for_status()是在get的过程中，如果不分析状态码，当418时也会是输出成功，只是没内容，不会抛出异常


10.处理数据的时候，需要通过print(type)去查看类型，如果是字典再分析通过键值和自己构建一个新字典，去保留需要的信息


11.函数返回信息的格式最好统一化，便于维护

---

## Day3
1.异步的价值在于并发，真正省的是在等待期间，程序可以去处理其他事情


2.异步使用场景一般有：高并发 I/O 场景、需要同时处理多件事、Web 框架 / 服务器、前端 / UI 编程


3.异步也会使代码更复杂；需要异步库；调试更难；计算密集用异步没用，需要上多线程


4.在调用大模型时，一定要控制system prompt，不然会让结果失控，无法达到预期效果


5.json文本返回到python是一种list（dict）格式，所以在增加内容时，要确保是一个list


6.json文件无法实现追加，需要将追加转换为:提取，添加再重写


7.在调用大模型API时可以参考官方API文档，通过那些示例代码可以更好上手


8.在设计程序时要考虑会出现的异常，需要考虑异常处理


## Day4
今天：阅读了部分httpx官方文档的QuickStart，对Day0任务进行完整解读，异步处理并发已经实现


**难点**：


    1.对字典进行排序取次数前十的处理：
        top10 = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]
            - sorted()函数的参数：传入被处理数据，排序规则，reverse确定是否降序
            - 由于定义的那个d[]为字典格式，字典无法排序，通过d.items()将字典转换成元组
            - 因为要按照次数进行排序，key默认是取第一个元素，但次数在d[1]的位置，所以需要通过一个函数去自定义返回值，确保按指定规则排序
              这里使用一个匿名函数lambda，使代码更紧凑
            - 通过reverse控制是否降序，默认的是升序，然后配合切片[:10]取前十名，或者指定的区间
    
明天：分析并发实现逻辑，完成剩余复盘任务，半小时文档阅读


1.还需要强化的单词


    explicit / explicitly   - 显式
    binary                  - 二进制
    access / accessed       - 访问
    custom                  - 自定义的
    keyword argument        - 关键字参数

2.python文件读取的方式：


        遍历对象	               每次拿到
    for x in "hello"	       一个字符（h, e, l, l, o）
    for x in ["a", "b"]	       一个列表元素
    for line in f（文件）	       一行（字符串）
    在读取文件时，默认是按行读取，如果要实现按字符读取文件，必须先f.read()把整个文件夹变成一个字符串，再读取

3.split() 的作用是按空白（空格、换行、Tab）把字符串切开，返回一个列表


    细节处理：
            - 1）不带参数时，按"任意空白"切
            - 2）它会顺手把换行符 \n 去掉了
            - 3）如果带参数，就按指定字符切
            - 4）如果处理连字符断词，一行没写完的情况，需要先f.read()读取整片，再合并断词.replace("-\n", ""),再考split()分词
    优化：用更聪明的分词（NLP 库）
    对于 PDF 提取的文本，一般用 re 正则或专门的库（如 pdfplumber）在提取阶段就处理好断行，而不是在词频统计阶段补救。

4.在处理记数的时候，使用get去更改键的值。get 的价值就是"键不存在时不报错，给个兜底值"  

```更好的代替：现在可以用collections.Counter或者collections.defaultdict
        from collections import defaultdict
            d = defaultdict(int)     # 默认值是 0（int() 返回 0）
                for word in line.split():
                d[word] += 1   
                ’‘’
          - from collections import Counter
            words = []
                for line in f:
                words.extend(line.split())
            d = Counter(words)       # 直接统计好词频

```

## Day5
今天：阅读HPPTX官方文档，


难点：

明天：

1.还需要强化的单词：

```
custom       自定义的、定制的

additional      额外的、附加的

outgoing      发出的、传出的

keyword argument      关键字参数

complicated      复杂的

instead      代替、转而、反而

generator      生成器

inspect      检查、查看

text phrase      文本短语

instance      实例

method      方法

interface      接口

case-insensitive      不区分大小写的

capitalization      大小写形式

recipient      接收方

semantics      语义

subsequent      随后的、后续的
    
```

2.在并发异步实现之中,用列表解包实现多个任务

```   
元组、生成器、集合、任何可迭代对象都能被 * 解包;
列表是最自然的"收集容器"；
列表推导式写起来最简洁，[f(i) for i in ...] 天然生成列表；
列表有序，能保证 gather 的返回顺序和你的预期一致；
列表可读性强，一看就知道是"一批任务"    
```
## Day6

今天：分析了投简历与打基础之间的规划，在处理文件之中，新增考虑**备份**问题,学习SQLite基本操作

难点：

明天：继续学完SQLite操作，解决毕设L1:模拟传感器 + SQLite


1.在Day0的基础上，添加读一个 JSON 文件 → 改一个字段 → 写回去部分功能

```
1.在处理JSON修改的时候，首先要考虑其中存放的数据是什么格式的
        JSON	        Python
        object {}	dict
        array []	list
        string ""	str
        number	        int / float
        true / false	bool
        null	        None
不同类型数据操作的方法不同

2.在提取JSON数据的时候，需要去考虑的方向：
    顶层类型检查 - 当你如果只设置了一种格式去读取，当格式不同时就会报错
    元素类型检查 - 里面的元素类型也需要坚持，如果类型不符也需要报错 

3.在修改文件的时候，也需要对原文件考虑一个备份问题
    技术实现：通过shutil.copy（path，path.with_suffix（".json.bak"））进行备份
   
4.强化isinstance函数的用法，判断一个对象是不是某个类型，返回一个bool值
```

2.SQLite的操作部分放在SQLite文件内，待写完

---

## Day7
今天：先补充完SQLite操作，学习MQTT传输协议内容

难点：在毕设设计，大模型部分，设计LangGragh的流程又忘记了，之前写的没印象

明天：先复习LangGraph语法部分，实现最小闭环

1.SQLite语法的关键：

```
代码	                        比喻	        作用
conn = sqlite3.connect(...)	打开本子	        建立连接
c = conn.cursor()	        拿笔	        创建游标，用来执行 SQL
c.execute(...)	                写字	        执行一条 SQL
conn.commit()	                按保存	        让增删改真正生效
conn.close()	                合本子	        关闭连接
```


---

## Day8
今天:阅读了FastAPI官方文档、体验接口功能和页面调试、学习了通过接口api来实现简单的增删改查操作

难点：

明天：把增删改查接入到本地文里

1.在FastAPI中输入路径参数的时候，要注意顺序，在下面这种场景，要先找me的和其他id的
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
 
```

2.如果路径操作接收一个路径参数，但希望可能有效的路径参数值是预设的，可以使用标准 Python Enum。以下通过python枚举和获取枚举值的方法去得到值
```py
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}    
```
3.在参数的选择中，只要是函数参数，且名字没有出现在大括号里，那它就是查询参数，并且查询参数如果没有设置默认值，就会默认必填，不写会报错

4.在HTTP协议中，没有规定某种方法代表什么功能，GET、POST、PUT、DELETE 只是名字不同，它们都能携带路径参数、查询参数和请求体（Body）；在 FastAPI 里写一个带路径参数和查询参数的 POST 请求时，它执行的命令本质上仍然是：“向指定的 URL 提交一份数据（Body），同时附带一些附加条件（Path/Query）。”

5.在查询参数需要添加约束的情况，可以通过Annotated和Query实现
```py
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```
这样可以实现，约束q是可以选，但如果有参数，其长度不超过50个字符

6.Annotated在FastAPI里的三大经典用途：
    1）强制指定参数类型（Query，Path，Body，Header）
    2）请求体的多参数（多个Pydantic模型）
    3）依赖注入（Dependencies）


## Day9
今天：完成FastAPI加json文件读写，实现本地文件管理数据；

难点：1.if any(t.id == thing.id for t in todo_list):
            any 是 Python 内置函数：只要可迭代对象里有任意一个值为真（truthy），就返回 True；全为假才返回 False。
            这是属于生成器语法：（表达式  for 变量 in 可迭代对象  [if 过滤条件]）
           2. sqlalchemy的分层，每一个模块负责的功能难以理解


明天：

1.pydantic的作用就是在一个文件里，事先定义好一个个类，里面写了一些必须的参数和参数类型，然后在函数输入或输出的参数里，加入定义好的类实现检验；它还可以自动生成JSON Schema，在Field里写的description、example，都会直接出现在Swagger UI文档里            

2.文件分层，可以实现更好的调试，把每一个部分的功能，存在每一个不同的文件里
    主要优势：
                    实现职责分层
                    可读性与定位极快
                    可测试
                    可拓展性
    企业级项目分层一般有3/4层：
                1.路由层（Router / API）：处理 HTTP 请求、依赖注入（你现在的 main.py）。
                2.业务逻辑层（Service）：处理核心业务逻辑（例如：发邮件、算折扣、权限判断）。
                3.数据访问层（Repository / CRUD）：专门写 SQL 增删改查的逻辑（比如 crud/todo.py）。
                4.模型层（Models / Schemas）：数据结构定义。

3.sqlalchemy的实现是先继承declarative_base()大类，通过定义类的方式去创建数据表,具体代码如下：
```py
Base = declarative_base()


class Person(Base):
    __tablename__ = "people"
    
    ssn = Column("ssn",Integer,primary_key=True)
    firstname = Column("firstname",String)
    lastname = Column("lastname",String)
    gender = Column("gender",CHAR)
    age = Column("age",Integer)

    def __init__(self,ssn,first,last,gender,age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age
#指定打印形式
    def __repr__(self):
        return f"({self.ssn}){self.firstname}{self.lastname}({self.gender},{self.age})"
```


4.所有模块里的依赖注入，本质都是为了切断组件之间的直接联系，把控制权反转（IoC）交给框架。这让你能专注写纯粹的业务逻辑，而不是陷在“连接、关闭、清理”的无底洞里。
依赖注入核心本质在解决以下四个问题：
                        1.解耦（把“使用”和“制造”分开）
                        2.自动化生命周期管理（只管借，不管还）
                        3.可替换性（方便测试 Mock）
                        4.声明式编程（少写代码，多看逻辑）

## Day10
今天：

难点：

明天：

1.无







