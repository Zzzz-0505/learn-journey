#目标：建立一个对照组，后面才知道分层解决了什么问题。
# □ 用 FastAPI 写一个 main.py，内存里用一个 list[dict] 存"待办事项"（todo）
# □ 提供 4 个接口：POST /todos、GET /todos、GET /todos/{id}、DELETE /todos/{id}
# □ 所有逻辑（校验、增删查）全写在 main.py 里，故意不做任何校验和异常处理

# from fastapi import FastAPI,HTTPException
# from pydantic import BaseModel

# app = FastAPI()
# todo_list:list["things"]=[]

# class things(BaseModel):
#     id:int
#     content:str

# @app.post("/todos")
# async def add_todo(thing:things):
#     if any(t.id == thing.id for t in todo_list):
#         raise HTTPException(400,"thing already exist")
#     todo_list.append(thing)
#     return {"message":"add successful"}

# @app.get("/todos")
# async def get_todo():
#     if not todo_list:
#         return {"message":"there is nothing to do"}
#     return todo_list

# @app.get("/todos/{id}")
# async def get_specific_todo(id:int):
#     for t in todo_list:
#         if t.id == id:
#             return t
#     raise HTTPException(404,"thing no exist")

    

# @app.delete("/todos/{id}")
# async def del_todo(id:int):
#     for i, t in enumerate(todo_list):
#         if t.id ==id:
#             del todo_list[i]
#             return {"message":"delete successful"}
#     raise HTTPException(404,"thing no exist")


from sqlalchemy import create_engine,ForeignKey,Column,String,Integer,CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# save_db_path = "/Users/zzzz/Desktop/Learn-journey-git/week2/SQLite-SQLAlchemy/use-sqlalchemy-fastapi/db/todo.db"
# Base = declarative_base()

class Person(Base):
    __tablename__ = "People"
    ssn = Column("ssn",Integer,primary_key=True)
    name = Column("name",String)
    gender = Column("gender",CHAR)

    def __init__(self,ssn,name,gender):
        self.ssn = ssn
        self.name = name
        self.gender = gender

    def __repr__(self):
        return f"({self.ssn}) {self.name} {self.gender}"

# class todo(Base):
#     __tablename__ = "Thing"
#     tid = Column("id",Integer,primary_key=True)
#     content = Column("content",String)
#     owner = Column(Integer,ForeignKey("People.ssn"))

#     def __init__(self,tid,content,owner):
#         self.tid = tid
#         self.content = content
#         self.owner = owner 

#     def __repr__(self):
#         return f"{self.owner} have these {self.tid}{self.content}to do. "

# engine = create_engine(f"sqlite:///{save_db_path}",echo=True)
# Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Person(13312,"张三","男")
p2 = Person(13313,"李四","男")
p3 = Person(13314,"王五","男")

session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

t1 = todo(1,"做作业",p1.ssn)
t2 = todo(2,"打游戏",p1.ssn)
t3 = todo(3,"看电视",p2.ssn)
t4 = todo(4,"跑步",p2.ssn)
t5 = todo(5,"打羽毛球",p3.ssn)
t6 = todo(6,"烧菜",p3.ssn)

session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.add(t5)
session.add(t6)
session.commit()

result = session.query(todo,Person).filter(Person.name == "张三").filter(todo.owner == Person.ssn).all()
for r in result:
    print(r)