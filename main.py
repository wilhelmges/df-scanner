from fastapi import FastAPI
from sqladmin import Admin

from db import engine, Base

# імпорт моделей ОБОВ'ЯЗКОВИЙ
from models.dbf110 import Df1

from admin.views import Df1Admin


app = FastAPI()

# створення таблиць Base.metadata.create_all(engine)
# sqladmin
admin = Admin(app, engine)

# реєстрація admin view
admin.add_view(Df1Admin)