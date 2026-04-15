from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_Avilable:str | None = "May be after One week"
    


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/details")
def detail(detail:Item):
    return{"name":detail.name,"price":detail.price,"Avilable":detail.is_Avilable}