from fastapi import FastAPI,Query,HTTPException
from pydantic import BaseModel
from typing import Annotated
from  pathlib import Path
import json


app = FastAPI()



# @app.get("/")
# def read_root():
#     return {"Hello":"World"}



#路径参数

#为指定路径设定预设值
# from enum import Enum


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet: #比较枚举成员
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet": #获取枚举值
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# #查询参数

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


#请求体
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# #请求体 + 路径参数 + 查询参数
# @app.post("/items/{item_id}")
# async def update_item(item_id:int,item: Item,q:str | None = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result


#查询参数与字符串校验
# @app.get("/items")
# async def read_items(
#     q:Annotated[
#         str | None ,
#         Query(
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             max_length=50,
#             deprecated=False,#控制弃用
#             ),
#             ]= None,
#             ):
#     results = {"items":[{"item_id":"Foo"},{"item_id":"Bar"}]}
#     if q:
#         results.update({"q":q})
#     return results


class Item(BaseModel):
    name:str
    prize:float

fake_db = {}
path = Path(__file__).parent / "history.json"

def open_file() ->dict:
    if not path.exists():
        return {}
    with open(path,"r",encoding="utf-8")as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}

def save_file(data):
    with open(path,"w",encoding="utf-8")as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    db = open_file()
    key = str(item_id)
    if key not in db:
        raise HTTPException(404, "not found this goods")
    return db[key]

@app.post("/items/{item_id}")
async def create_item(item_id:int,item:Item):
    db = open_file()
    key = str(item_id)
    if key in db:
        raise HTTPException(404, "this goods already exist")
    db[key] = item.model_dump()
    save_file(db)
    return {"message":"save successful","data":db[key]}

@app.put("/items/{item_id}")
async def updata_item(item_id:int,item:Item):
    db = open_file()
    key = str(item_id)
    if key not in db:
        raise HTTPException(404, "not found this goods")
    db[key] = item.model_dump()
    save_file(db)
    
    return {"message":"updata successful","data":db[key]}

@app.delete("/items/{item_id}")
async def delete_item(item_id:int):
    db = open_file()
    key = str(item_id)
    if key not in db:
        raise HTTPException(404, "not found this goods")
    del db[key]
    save_file(db)
    return{"message":"delete successful"}