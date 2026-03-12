import os


from fastapi import FastAPI, Depends
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from api_rest.conf.db import SessionLocal
from api_rest.conf.security import create_access_token
from api_rest.conf.security import verify_token


from api_rest.models.user import User
from api_rest.schemas.user import UserCreate, UserResponse

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





@app.post("/users")
def create_user(    user: UserCreate,
    db: Session = Depends(get_db),
    token=Depends(verify_token)):

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/token")
def login(username: str, password: str):

    # autenticación simple (puedes luego validar en DB)
    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }