from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text


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
        rows = [
            {
                "ipn": "1234567890",
                "lastname": "Іваненко"
            },
            {
                "ipn": "9876543210",
                "lastname": "Петренко"
            },
            {
                "ipn": "5555555555",
                "lastname": "Шевченко"
            }
        ]

        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    NUMIDENT as ipn,
                    LN as lastname
                FROM df1s
                LIMIT 10
            """))

        rows = result.mappings().all()

        return await self.templates.TemplateResponse(request, "simplepage.html",{
                "rows": rows
            })

admin.add_view(ReportView)

admin.add_view(Df1Admin)