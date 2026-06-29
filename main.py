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

#this is comment

@app.get("/")
def read_root():
    return {"Hello": "World"}


# ---------------- READ ALL ---------------- 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
 return {"item_id": item_id, "q": q}

# ---------------- CREATE ----------------

@app.post("/items")
def create_item(
    name: str,
    description: str,
    quantity: int,
    price: float,
    status: str,
    db: Session = Depends(get_db)
):

    item = Item(
        name=name,
        description=description,
        quantity=quantity,
        price=price,
        status=status
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Item Created Successfully",
        "data": item
    }


# ---------------- UPDATE ----------------

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    name: str,
    description: str,
    quantity: int,
    price: float,
    status: str,
    db: Session = Depends(get_db)
):

    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    item.name = name
    item.description = description
    item.quantity = quantity
    item.price = price
    item.status = status

    db.commit()
    db.refresh(item)

    return {
        "message": "Item Updated Successfully",
        "data": item
    }

# ---------------- DELETE ----------------

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    db.delete(item)
    db.commit()

    return {
        "message": "Item Deleted Successfully"
    }