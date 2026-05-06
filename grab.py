import dbf
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models.dbf110 import PaymentRecord
from db import Base, engine, SessionLocal

table = dbf.Table("j0510110_10_2025.dbf", codepage='cp1251')
table.open()
print(table.structure())

session = SessionLocal()

for record in table[:25]:
    print(record.NUMIDENT)
    session.add(PaymentRecord(
        NUMIDENT=record.NUMIDENT,
        PERIOD_M=record.PERIOD_M,
        PERIOD_Y=record.PERIOD_Y,
        LN=record.LN,
        NM=record.NM,
        SUM_NARAH=record.SUM_NARAH
    ))

session.commit()