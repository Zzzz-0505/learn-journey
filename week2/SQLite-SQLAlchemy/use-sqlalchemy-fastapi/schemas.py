from pydantic import BaseModel,Field

class TodoCreate(BaseModel):
    tid:int = Field(...,gt=0,description="主键必须大于0")
    content:str = Field(...,min_length=1,max_length=100,description="代办内容")

class TodoResponse(BaseModel):
    tid:int
    content:str

    class config():
        from_attributes = True

class TodoUpdate(BaseModel):
    content:str = Field(...,min_length=1)
    