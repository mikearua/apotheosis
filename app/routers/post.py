
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional
from .. import models, schemas, oauth2, utils
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

#, response_model=list[schemas.response]
@router.get("/", response_model=list[schemas.Out])
def get_posts(db: Session = Depends(get_db), user_id = Depends(oauth2.get_current_user),
              Limit:int = 30, skip:int = 0, search: Optional[str]= ""):
    #post = db.query(models.PostMethod).filter(models.PostMethod.title.contains(search)).limit(Limit).offset(skip).all()
    
    posts = db.query(models.PostMethod, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id==models.PostMethod.id, isouter=True).group_by(models.PostMethod.id).filter(
            models.PostMethod.title.contains(search)).limit(Limit).offset(skip).all()
        
    print(posts)
    print(Limit) 
    return posts
    

@router.get("/{id}", response_model=schemas.Out)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.PostMethod, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id==models.PostMethod.id, isouter=True).group_by(models.PostMethod.id).filter(
            models.PostMethod.id== id).first()
    if post == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")
    
               
    print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def post(var: schemas.createPost, db: Session = Depends(get_db), user_id = Depends(oauth2.get_current_user)):
    print(user_id.email)
    
    new_post = models.PostMethod(**var.dict(),
                                 owner_id=user_id.id)  #we add this line to connect the user_id to specific posts
    db.add(new_post) #to add to our database
    db.commit() # to commit to our database
    db.refresh(new_post) #to refresh the database to show the new post
    
    return new_post #returns the post to our API server

@router.put("/{id}", response_model=schemas.Response, )
def putt(id: int, var: schemas.update, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.PostMethod).filter(models.PostMethod.id== id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="you are not authorized to perform this action")
            
    post_query.update(var.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()
        
@router.delete("/{id}")
def dele(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.PostMethod).filter(models.PostMethod.id== id)
    #we are defining the post query
    
    post = post_query.first() # gettin the first post that the query returns
    
    if post == None: #if the first post bearing the id doesnt exist
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")
    
    if post.owner_id != user_id.id:
        #if the user who is actually logged in owns this post
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="you are not authorized to perform this action")
            
    post_query.delete(synchronize_session=False) #deleting wht the query return
    db.commit()
        
    return Response(status_code = status.HTTP_204_NO_CONTENT)
        