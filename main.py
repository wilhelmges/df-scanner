from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose
# імпорт моделей ОБОВ'ЯЗКОВИЙ
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5
from admin.auth import AdminAuth
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
authentication_backend = AdminAuth(
    secret_key="FES_SECURITY_KEY"
)
admin = Admin(app, engine, templates_dir="templates", authentication_backend=authentication_backend,)

from models.dbf110 import Df1
from admin.views import Df1Admin, Df4Admin, Df5Admin

from admin.notvalid_ipns import NotvalidIpns
from admin.pib_withdifferent_ipns import PibWithDifferetIpns
from admin.ipn_withdiffpibs import IpnWithDiffPibs
from admin.sample_view import SampleReportView

admin.add_view(Df1Admin)
admin.add_view(Df4Admin)
admin.add_view(Df5Admin)

admin.add_view(NotvalidIpns)
admin.add_view(PibWithDifferetIpns)
admin.add_view(IpnWithDiffPibs)
#admin.add_view(SampleReportView)

