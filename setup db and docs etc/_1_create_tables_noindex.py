from db import engine
from models.sqlmodels import Df1, Df4, Df5

Df1.__table__.create(engine, checkfirst=True)
Df4.__table__.create(engine, checkfirst=True)
Df5.__table__.create(engine, checkfirst=True)