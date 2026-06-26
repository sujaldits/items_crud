from fastapi import FastAPI
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
app = FastAPI()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    quantity = Column(Integer, index=True)
    price = Column(Float, index=True)
    status = Column(String(50), index=True)

# this is comment

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
 return {"item_id": item_id, "q": q}

