from sqlalchemy import create_engine,ForeignKey,Column,String,Integer,CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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



class Thing(Base):
    __tablename__ = "things"

    tid = Column("id",Integer,primary_key=True)
    description = Column("description",String)
    owner = Column(Integer,ForeignKey("people.ssn"))

    def __init__(self,tid,description,owner):
        self.tid = tid
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"({self.tid}){self.description} owned by {self.owner}"
        
engine = create_engine("sqlite:///mydb.db",echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# person = Person(12312,"Mike","Smith","m",35)
# session.add(person)
# session.commit()

# p1 = Person(14324,"Anna","Smith","f",40)
# p2 = Person(12314,"Bnna","Smith","m",24)
# p3 = Person(15443,"Cnna","Smith","m",19)

# session.add(p1)
# session.add(p2)
# session.add(p3)

# session.commit()


#SELECT
# result = session.query(Person).all()
# print(result)

# result1 = session.query(Person).filter(Person.firstname == "Anna")
# for r in result1:
#     print(r)

# result2 = session.query(Person).filter(Person.age > 25)
# for r in result2:
#     print(r)

# result3 = session.query(Person).filter(Person.firstname.like("%An%"))
# for r in result3:
#     print(r)

# result4 = session.query(Person).filter(Person.firstname.in_(["Anna","Bnna"]))
# for r in result4:
#     print(r)


# t1 = Thing(1,"Car",p1.ssn)
# t2 = Thing(2,"iphone18",p2.ssn)
# t3 = Thing(3,"Computer",p3.ssn)
# t4 = Thing(4,"Apple",p1.ssn)
# t5 = Thing(5,"house",p2.ssn)

# session.add(t1)
# session.add(t2)
# session.add(t3)
# session.add(t4)
# session.add(t5)
# session.commit()

result = session.query(Thing,Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna").all()
for r in result:
    print(r)