from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine

app = FastAPI()
admin = Admin(app, engine, templates_dir="templates")

from models.dbf110 import Df1
from admin.views import Df1Admin

from sqladmin import BaseView, expose

class ReportView(BaseView):
    name = "Report Page"
    icon = "fa-solid fa-chart-line"


    @expose("/report", methods=["GET"])
    async def report_page(self, request):
        return await self.templates.TemplateResponse(request, "simplepage.html")

admin.add_view(ReportView)

admin.add_view(Df1Admin)