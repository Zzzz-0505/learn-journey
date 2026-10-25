#管形状
#它定义的是"数据在跨越边界时的形状"，不是"待办清单"本身。这里的"边界"指：

from pydantic import BaseModel,Field
from datetime import date
from typing import Literal


class TodoCreate(BaseModel):
    title:str = Field(min_length=1,max_length=20)
    deadline:date
    level:Literal[1,2,3]

class TodoOut(BaseModel):
    id:int
    title:str
    deadline:date
    level:Literal[1,2,3]

    model_config = {"from_attributes":True}


