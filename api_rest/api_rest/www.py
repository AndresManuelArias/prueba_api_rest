import os


from fastapi import FastAPI, Depends,Query
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy import select
from api_rest.conf.db import SessionLocal
from api_rest.conf.db import Base, engine
from typing import List

from api_rest.conf.security import create_access_token
from api_rest.conf.security import verify_token




from api_rest.models.user import User
from api_rest.schemas.user import UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

static_file_path = os.path.dirname(os.path.realpath(__file__)) + "/static"
app.mount("/static", StaticFiles(directory=static_file_path), name="static")


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}


@app.post("/token")
def login(username: str, password: str):

    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password

    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return db_user


from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_

@app.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a devolver"),
    email: str = Query(None, description="Filtrar usuarios por correo (parcial o completo)"),
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    users = query.offset(skip).limit(limit).all()
    return users


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token=Depends(verify_token)
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()

    return