from db import engine
from models.sqlmodels import Df1

Df1.__table__.create(engine, checkfirst=True)