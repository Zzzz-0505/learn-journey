from fastapi import FastAPI,Query,HTTPException
from pydantic import BaseModel
from typing import Annotated


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

@app.get("/items/{item_id}")
async def create_item(item_id:int):
    if item_id  not in fake_db:
        raise HTTPException(status_code=404,detail="not found this goods")

    return fake_db[item_id]

@app.post("/items/{item_id}")
async def read_item(item_id:int,item:Item):
    if item_id  in fake_db:
        raise HTTPException(status_code=400,detail="ID already exist")
    fake_db[item_id] = item.model_dump()
    return {"message":"save successful","data":fake_db[item_id]}

@app.put("/items/{item_id}")
async def updata_item(item_id:int,item:Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404,detail="not found this goods")
    fake_db[item_id] = item.model_dump()
    return {"message":"updata successful","data":fake_db[item_id]}

@app.delete("/items/{item_id}")
async def delete_item(item_id:int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404,detail="not found this goods")
    del fake_db[item_id]
    return{"message":"delete successful"}