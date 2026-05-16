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
        Df1.PAY_MNTH == shape.PAY_MNTH,
        Df1.PAY_TP == shape.PAY_TP,
    )
    result = session.execute(stmt).scalar_one()
    if result is None:
        raise Exception("Не знайдено")
    else:
        session.delete(result)

def add_df1(rerec: SimpleNamespace, session):
    session.add(Df1(
        PERIOD_M=rerec.PERIOD_M,
        PERIOD_Y=rerec.PERIOD_Y,
        NUMIDENT=str(rerec.NUMIDENT),
        LN=rerec.LN,
        NM=rerec.NM,
        FTN=rerec.FTN,

        PAY_TP=rerec.PAY_TP,
        PAY_MNTH=rerec.PAY_MNTH,
        PAY_YEAR=rerec.PAY_YEAR,

        SUM_TOTAL=rerec.SUM_TOTAL,
        SUM_MAX=rerec.SUM_MAX,
        SUM_INS=rerec.SUM_INS,
        SUM_NARAH=rerec.SUM_NARAH,
        OZN=rerec.OZN
    ))

def inc_or_create(rerec: SimpleNamespace, session):
    stmt = select(Df1).where(
        Df1.NUMIDENT == rerec.NUMIDENT,
        Df1.PERIOD_M == rerec.PERIOD_M,
        Df1.PERIOD_Y == rerec.PERIOD_Y,
        Df1.PAY_YEAR == rerec.PAY_YEAR,
        Df1.PAY_MNTH == rerec.PAY_MNTH,
    )
    obj = session.execute(stmt).scalar_one_or_none()
    if obj is None: # we need to add record
        add_df1(rerec, session)
        return
    obj.SUM_NARAH += Decimal(str(rerec.SUM_NARAH))

def dec_or_delete(rerec: SimpleNamespace, session):
    stmt = select(Df1).where(
        Df1.NUMIDENT == rerec.NUMIDENT,
        Df1.PERIOD_M == rerec.PERIOD_M,
        Df1.PERIOD_Y == rerec.PERIOD_Y,
        Df1.PAY_YEAR == rerec.PAY_YEAR,
        Df1.PAY_MNTH == rerec.PAY_MNTH,
    )
    obj = session.execute(stmt).scalar_one()
    diffnarah = obj.SUM_NARAH - Decimal(str(rerec.SUM_NARAH))
    if diffnarah == 0:
        session.delete(obj)
        return
    if float(abs(diffnarah)) < 0.01:
        raise Exception('maybe delete? ')
    obj.SUM_NARAH-=Decimal(str(rerec.SUM_NARAH))

def incdec_df1_record(shape: SimpleNamespace, session):
    obj = session.execute(
        select(Df1).where(
            Df1.NUMIDENT == shape.NUMIDENT,
            Df1.PERIOD_M == shape.PERIOD_M,
            Df1.PERIOD_Y == shape.PERIOD_Y,
            Df1.PAY_YEAR == shape.PAY_YEAR,
            Df1.PAY_MNTH == shape.PAY_MNTH,
        )
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