from jose import jwt, JWTError # pip install python-jose[cryptography]
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic.networks import EmailStr
from . import schemas
from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function that create our JWT  
def create_access_token(data: dict):
    # copy the dictionary into "to_ecoded"
    to_encode = data.copy()

    # Create the Expire Time (now + 30)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

   # Update the dictionary exp to the expire time that we create 
    to_encode.update({"exp": expire})

    # Create our JWT with the spesific infos, secret_key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # return it
    return encoded_jwt




# Crete a Function that Verify our Access token
def verify_access_token(token: str, credentials_exception):
    
    try:
        # decode the token and store it in payload
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # get the user_id from the payload
        email: EmailStr = payload.get("user_email") # get the user_email from the payload
        #print(payload)

        # check the id existance
        if id is None:
            raise credentials_exception

        # create an instance of TokenData paydantic and return it
        token_data = schemas.TokenData(id=id, email=email)

    # raising credentials_exception that we take it from parametres
    except JWTError:
        raise credentials_exception

    return token_data


# Function for getting data from the token (calling the verify_access_token) with credentials_exception
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"www-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user

