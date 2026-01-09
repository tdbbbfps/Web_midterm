from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_database
from . import models, schemas, service
from datetime import timedelta
from auth.jwt import create_access_token, get_token_expire_time

router = APIRouter()

@router.post('/create', response_model=schemas.User)
async def create_user(user : schemas.UserCreate, db : Session = Depends(get_database)):
    try:
        db_user = service.create_user(db, user)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered or password too weak.")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post('/login')
async def login(user: schemas.UserLogin, db: Session = Depends(get_database)):
    try:
        db_user = service.get_user_by_username(db, user.username)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        if not service.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        access_token_expires = timedelta(minutes=get_token_expire_time())
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/read', response_model=schemas.User)
async def read_user(user_id : int, db : Session = Depends(get_database)):
    try:
        user = service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put('/update', response_model=schemas.User)
async def update_user(user_id: int, user_update : schemas.UserUpdate, db : Session = Depends(get_database)):
    try:
        db_user = service.update_user(db, user_id, user_update)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/delete')
async def delete_user(user_id : int, db : Session = Depends(get_database)):
    try:
        success = service.delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User deleted successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
