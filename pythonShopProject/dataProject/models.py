from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserModel(BaseModel):
    username:str
    email:str
    password:str

class LogInModel(BaseModel):
    username:str
    password:str

class shopCreateModel(BaseModel):
    user_id:int
    shop_name:str

class addProduct(BaseModel):
    product_name:str
    category_id:int
    product_store_id:int
    product_price:int


class productOrder(BaseModel):
    product_id:int
    store_id:int
    user_ordering:int
    order_address:str
    order_date:str


class getCart(BaseModel):
    user_id:int
    store_id:int

class updatingOrders(BaseModel):
    order_ids:List[int]
    order_address:str

class addRating(BaseModel):
    user_id:int
    store_id:int
    rate:int

class checkRelation(BaseModel):
    user_id:int
    store_id:int

class gettingPoints(checkRelation):
    pass

class updatePoints(BaseModel):
    user_id:int
    store_id:int
    points:int

