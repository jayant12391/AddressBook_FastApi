from sqlalchemy.orm import Session
from app.models import Address
from app.schemas import AddressCreate

def create_address(db: Session, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address

def get_addresses_within_radius(db: Session, lat: float, lon: float, radius: float):
    addresses = db.query(Address).all()
    within_radius = []
    from geopy.distance import geodesic
    for address in addresses:
        if geodesic((lat, lon), (address.latitude, address.longitude)).km <= radius:
            within_radius.append(address)
    return within_radius
