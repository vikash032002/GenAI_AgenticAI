from pydantic import BaseModel

class UserEx(BaseModel):
    id:int
    name:str
    is_active:bool

input_obj={'id':101, 'name':'Vikash', 'is_active':True}

user=UserEx(**input_obj)
print(user);
