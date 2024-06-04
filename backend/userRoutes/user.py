from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import create_user, UserLogin
from getdb import get_db
from schema.schema import UserSchema
from datetime import datetime, timedelta
import jwt

# Secret key to encode and decode the JWT token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post('/signup', response_model=create_user)
async def register_user(user: create_user, db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="User is required")

        db_user = UserSchema(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return create_user(**db_user.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post('/login')
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserSchema).filter(UserSchema.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.password != db_user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: timedelta    ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
