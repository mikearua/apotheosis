from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import second_engine, sec_db
from sqlalchemy.orm import Session
from sqlalchemy import delete

models.Base.metadata.create_all(bind=second_engine)

app = FastAPI()

class Schema(BaseModel):
    title: str
    data: str
         #server: str
    published:bool = True
    
try:
    conn = psycopg2.connect(host='localhost', database='testing', user='postgres', password='marvel2127', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connected")
except Exception as error:
    print("connection failed")
    print("error", error)
    time.sleep(2)
    
    
    
@app.get("/")
def home():
    return{"msg": "welcome"}

@app.get("/posts")
def posts(db: Session = Depends(sec_db)):
    post = db.query(models.Another).all()
    return{"posts": post}
    

@app.post("/another")
def post(var: Schema, db: Session = Depends(sec_db)):
    post = models.Another(**var.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return{"new post": post}

@app.get("/another/{id}")
def gett(id: int, db: Session = Depends(sec_db)):
    post = db.query(models.Another).filter(models.Another.id == id).first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")
    
    return {"post": post}
    
@app.put("/another/{id}")
def update(id: int,var: Schema, db: Session = Depends(sec_db)):
    query = db.query(models.Another).filter(models.Another.id==id)   
    post = query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")
    
    query.update(var.dict(), synchronize_session=False)
    
    db.commit()
    return{"updated post": query.first()}

@app.delete("/another/{id}")
def dele(id:int, db: Session = Depends(sec_db)):
    post = db.query(models.Another).filter(models.Another.id==id) 
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id: {id} is not found")
       
    post.delete(synchronize_session=False)    
    db.commit()
    return{"post deleted"}