from sqlalchemy import create_engine, select, delete, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError
from core import to_int
from decimal import Decimal


from db import Base, engine, SessionLocal
from models.dbf110 import Df1
from types import SimpleNamespace

def delete_from_df1():
    with SessionLocal() as session:
        session.execute(delete(Df1))
        session.commit()

def finddf1(shape: SimpleNamespace):

    with SessionLocal() as session:
        stmt = select(Df1).where(
            Df1.NUMIDENT == shape.NUMIDENT,
            Df1.PERIOD_M == shape.PERIOD_M,
            Df1.PERIOD_Y == shape.PERIOD_Y,
            Df1.PAY_YEAR == shape.PAY_YEAR,
            Df1.PAY_MNTH == shape.PAY_MNTH
        )
        try:
            result = session.execute(stmt).scalar_one_or_none()
            #result = session.execute(stmt).scalars().all()
            if result is None:
                print("Не знайдено")
            else:
                print("Знайдено:", result)
                return result

        except MultipleResultsFound:
            print("Помилка: знайдено більше одного запису")

def find_df1_anddeleteifonlyone(shape: SimpleNamespace, session):
    stmt = select(Df1).where(
        Df1.NUMIDENT == shape.NUMIDENT,
        Df1.PERIOD_M == shape.PERIOD_M,
        Df1.PERIOD_Y == shape.PERIOD_Y,
        Df1.PAY_YEAR == shape.PAY_YEAR,
        Df1.PAY_MNTH == shape.PAY_MNTH
    )

    result = session.execute(stmt).scalar_one_or_none()
    if result is None:
        raise Exception("Не знайдено")
    else:
        print("Знайдено:", result)
        session.delete(result)

def add_df1(shape: SimpleNamespace, session):
    session.add(Df1(
        NUMIDENT=shape.NUMIDENT,
        PERIOD_M=shape.PERIOD_M,
        PERIOD_Y=shape.PERIOD_Y,
        PAY_YEAR=shape.PAY_YEAR,
        PAY_MNTH=shape.PAY_MNTH
    ))

def incdec_df1_record(shape: SimpleNamespace, session):
    obj = session.execute(
        select(Df1).where(Df1.id == 1)
    ).scalar_one()
    sign = -1 if to_int(shape.PAY_TP) == 3 else 1 if to_int(shape.PAY_TP) == 2 else None
    obj.SUM_NARAH += Decimal(sign*shape.SUM_NARAH)

if __name__ == "__main__":
    finddf1(SimpleNamespace(**{
    "NUMIDENT": "2663305759",
    "PERIOD_Y": 2025,
    "PERIOD_M": 5,
    "PAY_YEAR": 2024,
    "PAY_MNTH": 6
}))