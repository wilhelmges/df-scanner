from fastapi import FastAPI, Request
from sqladmin import Admin, BaseView, expose
from starlette.responses import HTMLResponse

from db import engine

# імпорт моделей ОБОВ'ЯЗКОВИЙ
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

from admin.views import Df1Admin, Df4Admin, Df5Admin
from admin.sql_views import SampleReportView

app = FastAPI()

# створення таблиць Base.metadata.create_all(engine)
# sqladmin
admin = Admin(app, engine, templates_dir="templates")

# реєстрація admin view
admin.add_view(Df1Admin)
admin.add_view(Df4Admin)
admin.add_view(Df5Admin)

class SimplePageView(BaseView):
    name = "Тест"
    category = "Звіти"

    @expose("/simplepage")
    async def index(self, request: Request):
        return await self.templates.TemplateResponse(
            request,
            "simplepage.html",  # templates/simplepage.html
            {}
        )


admin.add_view(SimplePageView)