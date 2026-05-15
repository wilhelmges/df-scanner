from fastapi import FastAPI
from sqladmin import Admin

from db import engine, Base

# імпорт моделей ОБОВ'ЯЗКОВИЙ
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

from admin.views import Df1Admin, Df4Admin, Df5Admin


app = FastAPI()

# створення таблиць Base.metadata.create_all(engine)
# sqladmin
admin = Admin(app, engine)

# реєстрація admin view
admin.add_view(Df1Admin)
admin.add_view(Df4Admin)
admin.add_view(Df5Admin)