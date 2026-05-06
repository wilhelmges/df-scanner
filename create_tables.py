from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from db import Base, engine, SessionLocal

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
from models.dbf110 import PaymentRecord


Base.metadata.create_all(engine)
session = SessionLocal()

session.add(User(name="Test"))
session.commit()