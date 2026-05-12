from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import MultipleResultsFound

from db import Base, engine, SessionLocal
from models.dbf110 import Df1
from types import SimpleNamespace

def finddf1(shape: SimpleNamespace):
    print(shape)
    with SessionLocal() as session:
        stmt = select(Df1).where(
            Df1.NUMIDENT == shape.NUMIDENT,
            Df1.PERIOD_M == shape.PERIOD_M,
            Df1.PERIOD_Y == shape.PERIOD_Y,
            Df1.PAY_YEAR == shape.PAY_YEAR,
            Df1.PAY_MNTH == shape.PAY_MNTH
        )

        try:
            #result = session.execute(stmt).scalar_one_or_none()
            result = session.execute(stmt).scalars().all()
            for r in result:
                print(r.NUMIDENT, r.LN)

            if result is None:
                print("Не знайдено")
            else:
                print("Знайдено:", result)

        except MultipleResultsFound:
            print("Помилка: знайдено більше одного запису")

if __name__ == "__main__":
    finddf1(SimpleNamespace(**{
    "NUMIDENT": "2663305759",
    "PERIOD_Y": 2025,
    "PERIOD_M": 5,
    "PAY_YEAR": 2024,
    "PAY_MNTH": 6
}))