from sqlalchemy.orm import Session
from . import models, schemas

def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(
        name=item.name,
        image=item.image,
        description=item.description,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_items(db: Session) -> list[models.Item]:
    return db.query(models.Item).all()

def get_item_by_id(db: Session, item_id: int) -> models.Item:
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate) -> models.Item:
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True
