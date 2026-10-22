#只验证"能连上 SQLite 并建一个空表“
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

#连接串
save_db_path = "/Users/zzzz/Desktop/Learn-journey-git/week2/SQLite-SQLAlchemy/use-sqlalchemy-fastapi/db/todo.db"

#engine：管连接
engine = create_engine(f"sqlite:///{save_db_path}",connect_args={"check_same_thread":False},echo=True)

#SessionLocal：会话工厂
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

#依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()