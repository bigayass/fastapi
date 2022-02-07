
from .. import models, schemas, oauth2, utils
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    users = db.query(models.User).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return new_user




@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")


    return user