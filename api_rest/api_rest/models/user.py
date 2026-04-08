from sqlalchemy import Column, Integer, String
from api_rest.conf.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)

    email = Column(String(100), unique=True, nullable=False, index=True)

    password = Column(String(200), nullable=False)