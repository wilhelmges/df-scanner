from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose
from core import check_tax_code, parse_ipn


class NotvalidIpns(BaseView):
    icon = "fa-solid fa-chart-line"
    category = 'Перевірочні звіти'

    name = "Невалідні ІПН"

    @expose("/report", methods=["GET"])
    async def report_page(self, request):
        raw_conn = engine.raw_connection()
        cursor = None
        try:
            raw_conn.create_function("check_tax_code", 1, check_tax_code)
            raw_conn.create_function("parse_ipn", 1, parse_ipn)
            cursor = raw_conn.cursor()

            result = raw_conn.execute("""
                    SELECT DISTINCT
        NUMIDENT AS ipn,
        TRIM(LN || ' ' || NM || ' ' || FTN) AS pib,
        parse_ipn(NUMIDENT) as ipndata
    FROM df1s
    WHERE
    NOT check_tax_code(NUMIDENT) AND
    NUMIDENT IS NOT NULL
     LIMIT 50
            """)
            #

            rows = [
                {
                    "ipn": row[0],
                    "pib": row[1],
                    "ipndata": row[2]
                }
                for row in result.fetchall()
            ]
            print('notipns ', len(rows))
        finally:
            cursor.close()
            raw_conn.close()

        return await self.templates.TemplateResponse(request, "notvalid_ipns.html", {
            "rows": rows
        })
