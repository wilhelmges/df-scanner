
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose
from core import check_tax_code, parse_ipn


class PibWithDifferetIpns(BaseView):
    icon = "fa-solid fa-chart-line"
    category = 'Перевірочні звіти'

    name = "ПІБ з різними ІПН"

    @expose("/diffipns", methods=["GET"])
    async def diffipns_page(self, request):
        raw_conn = engine.raw_connection()
        cursor = None
        try:
            raw_conn.create_function("check_tax_code", 1, check_tax_code)
            raw_conn.create_function("parse_ipn", 1, parse_ipn)
            cursor = raw_conn.cursor()

            result = raw_conn.execute("""
                   WITH persons AS (
    SELECT DISTINCT
        NUMIDENT AS ipn,
        TRIM(LN || ' ' || NM || ' ' || FTN) AS pib
    FROM Df1s
    WHERE
        NUMIDENT IS NOT NULL
        AND TRIM(NUMIDENT) <> ''
),
pib_counts AS (
    SELECT
        pib,
        COUNT(DISTINCT ipn) AS ipn_count
    FROM persons
    GROUP BY pib
    HAVING COUNT(DISTINCT ipn) > 1
)
SELECT DISTINCT
	p.ipn,
    p.pib,
    parse_ipn(p.ipn) AS ipndata
FROM persons p
JOIN pib_counts pc
    ON p.pib = pc.pib
ORDER BY
    pc.ipn_count DESC,
    p.pib ASC,
    p.ipn ASC;
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
