from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose

app = FastAPI()
admin = Admin(app, engine, templates_dir="templates")

from models.dbf110 import Df1
from admin.views import Df1Admin

from admin.notvalid_ipns import NotvalidIpns
from admin.sample_view import SampleReportView

admin.add_view(Df1Admin)
admin.add_view(NotvalidIpns)
admin.add_view(SampleReportView)

