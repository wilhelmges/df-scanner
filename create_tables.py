from sqlalchemy import Column, Integer, String

from db import Base, SessionLocal, engine
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)
session = SessionLocal()

session.add(User(name="Test"))
session.commit()
