from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_database
from . import models, schemas, service

router = APIRouter()

@router.post('/create', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_database)):
    try:
        db_item = service.create_item(db, item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/all', response_model=list[schemas.Item])
async def get_all_items(db: Session = Depends(get_database)):
    try:
        items = service.get_all_items(db)
        return items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/read', response_model=schemas.Item)
async def get_item(item_id: int, db: Session = Depends(get_database)):
    try:
        item = service.get_item_by_id(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="道具不存在")
        return item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put('/update', response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_database)):
    try:
        db_item = service.update_item(db, item_id, item)
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="道具不存在")
        return db_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/delete')
async def delete_item(item_id: int, db: Session = Depends(get_database)):
    try:
        success = service.delete_item(db, item_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="道具不存在")
        return {"message": "道具已成功刪除"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
