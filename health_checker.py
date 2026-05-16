from sqlalchemy import select
from db import SessionLocal, engine
from models.dbf110 import Df1

def check_ipns():
    with SessionLocal(engine) as session:
        stmt = select(Df1.NUMIDENT).distinct()
        result = session.execute(stmt).scalars().all()
        print(len(result))
