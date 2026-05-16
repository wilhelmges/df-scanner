from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose


class NotvalidIpns(BaseView):
    icon = "fa-solid fa-chart-line"
    category = 'Перевірочні звіти'

    name = "Невалідні ІПН"
    @expose("/report", methods=["GET"])
    async def report_page(self, request):


        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT DISTINCT
    NUMIDENT AS ipn,
    TRIM(LN || ' ' || NM || ' ' || FTN) AS pib
FROM df1s
WHERE CAST(NUMIDENT AS INTEGER) % 2 = 0
  AND NUMIDENT IS NOT NULL
 LIMIT 10
            """))

        rows = result.mappings().all()

        return await self.templates.TemplateResponse(request, "notvalid_ipns.html",{
                "rows": rows
            })