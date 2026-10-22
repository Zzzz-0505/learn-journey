from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.todo import Todo  
from db.database import engine, Base, get_db
from schemas import TodoCreate,TodoResponse,TodoUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.post("/todos",response_model=TodoResponse)
def add_todo(todo_in:TodoCreate,db: Session = Depends(get_db)):
    t1 = Todo(tid=todo_in.tid,content=todo_in.content)
    db.add(t1)
    db.commit()
    return t1
    


@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    result = db.query(Todo).all()
    return result



@app.get("/todos/{tid}")
def get_specific_todo(tid:int,db: Session = Depends(get_db)):
    result = db.query(Todo).filter(Todo.tid == tid).first()
    if not result:
        raise HTTPException(status_code=404,detail="Todo not found")
    return result
    


@app.put("/todos/{tid}")
def update_todo(tid:int,todo_in:TodoUpdate,db: Session = Depends(get_db)):
    result = db.query(Todo).filter(Todo.tid == tid).first()
    if result:
        result.content = todo_in.content
        db.commit()
        db.refresh(result)
        return {"content":"update successful"}
    else:
        raise HTTPException(status_code=404,detail="Todo not found")
    
  


@app.delete("/todos/{tid}")
def del_todo(tid:int,db: Session = Depends(get_db)):
    result = db.query(Todo).filter(Todo.tid == tid).first()
    if result:
        db.delete(result)
        db.commit()
        return {"content":"delete successful"}
    else:
        raise HTTPException(status_code=404, detail="This id does not exist")

    
    
