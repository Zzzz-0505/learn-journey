from sqlalchemy import Column,Integer,String,ForeignKey
from db.database import Base

class Todo(Base):
    __tablename__ = "Thing"
    tid = Column("id",Integer,primary_key=True)
    content = Column("content",String)
    # owner = Column(Integer,ForeignKey("People.ssn"))

    def __init__(self,tid,content):
        self.tid = tid
        self.content = content
        # self.owner = owner 

    def __repr__(self):
        return f" There are these {self.tid}.{self.content} to do. "