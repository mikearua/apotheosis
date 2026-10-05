
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, schemas, utils

router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def user(user: schemas.userCreate, db: Session = Depends(database.get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict()) 
    db.add(new_user) #to add to our database
    db.commit() # to commit to our database
    db.refresh(new_user) #to refresh the database to show the new post
    return new_user

#retrieve info based on user id

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
        
    return user

