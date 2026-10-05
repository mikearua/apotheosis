from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY
#ALGORITHM
#DURATION: EXPIRATION TIME

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): # data is saved as a dictionary obj
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #counting the time remaining from now
    
    to_encode.update({"exp": expire}) # updates our data with the countdown
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #creating the jwt token
#the parameters are what we want to add to our token
#the first is everythin we want to put into the payload, the second is the secret key(the signature) and then we specify the algorith   
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
    
        id: int = payload.get("user_id")
    
        if id == None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    
    
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id== token.id).first()
    
    return user