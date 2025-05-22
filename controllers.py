from sqlalchemy.orm import Session
from models import ItemDB
from schemas import *

def get_all_items(db: Session):
    test =  db.query(ItemDB).all()
    return [itemdb_to_Customers(test) for test in test]

def create_item(db: Session, item_data: CustomersGet):
    db_item = ItemDB(
        name=item_data.name,
        price=item_data.details.price,
        description=item_data.details.description,
        color=item_data.details.color,
        stock=item_data.stock
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return itemdb_to_Customers(db_item)

# Fonction pour mettre à jour un item
def update_item(db: Session, item_id: int, item_data: CustomersGet):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not db_item:
        return None
    db_item.name = item_data.name
    db_item.price = item_data.details.price
    db_item.description = item_data.details.description
    db_item.color = item_data.details.color
    db_item.stock = item_data.stock
    db.commit()
    db.refresh(db_item)
    return db_item

# Fonction pour supprimer un item
def delete_item(db: Session, item_id: int):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def itemdb_to_Customers(item: ItemDB) -> CustomersGet:
    return CustomersGet(
        name=item.name,
        details=Details(
            price=item.price,
            description=item.description,
            color=item.color
        ),
        stock=item.stock,
        id=item.id
    )