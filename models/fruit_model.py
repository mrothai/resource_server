from pydantic import BaseModel
from typing import Union

class FruitModel(BaseModel):
    name:str
    price:Union[int,None] = None