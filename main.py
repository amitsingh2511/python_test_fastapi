from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, condecimal
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Dadabase Urls
DATABASE_URL = "sqlite:///./pythontest.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Defining Database
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    village = Column(String, index=True)
    pincode = Column(String, index=True)
    distance = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Defined Users Request for create address.
class AddressCreate(BaseModel):
    village: str
    pincode: str
    distance: str
    state: str
    country: str

# Defined Users request for update address based on this columns.
class AddressUpdate(BaseModel):
    village: Optional[str]
    pincode: Optional[str]
    distance: Optional[str]
    state: Optional[str]
    country: Optional[str]

class SearchAddress(BaseModel):
    pincode: Optional[str]
    distance: Optional[str]
    state: Optional[str]

# Create Address using this api
@app.post("/addresses/")
def create_address(address: AddressCreate):
    db = SessionLocal()
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# Update Address using this api
@app.put("/addresses/{address_id}")
def update_address(address_id: int, address: AddressUpdate):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

# Delete Address using this api
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address

# Get Address By Search Criteria using this api
@app.get("/addresses/",)
def get_addresses(address: SearchAddress = Depends()):
    db = SessionLocal()
    db_address = db.query(Address).all()
    if address.state:
        db_address = db.query(Address).filter(Address.state == address.state).all()
    if address.distance:
        db_address = db.query(Address).filter(Address.distance == address.distance).all()
    return db_address

# Get Address By Id using this api
@app.get("/addresses/{address_id}")
def get_address_by_id(address_id: int):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
