from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------------- DATABASE ----------------

DATABASE_URL = "sqlite:///./items.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

app = FastAPI()

# ---------------- MODEL ----------------

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)
    status = Column(String(50))
    
# Create the table
Base.metadata.create_all(bind=engine)

# ---------------- DATABASE SESSION ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI CRUD"}

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

# ---------------- READ ALL ----------------

@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# ---------------- READ ONE ----------------

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item Not Found")

    return item

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

    if item is None:
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

    if item is None:
        raise HTTPException(status_code=404, detail="Item Not Found")

    db.delete(item)
    db.commit()

    return {
        "message": "Item Deleted Successfully"
    }