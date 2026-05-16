from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose


class SampleReportView(BaseView):
    icon = "fa-solid fa-chart-line"
    category = 'Перевірочні звіти'

    name = "Report Page"
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