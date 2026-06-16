from sqladmin import BaseView, expose

from core import parse_ipn
from db import engine


class IpnWithDiffPibs(BaseView):
    icon = "fa-solid fa-chart-line"
    category = 'Перевірочні звіти'

    name = "ІПН з різними ПІБ"

    @expose("/diffpibs", methods=["GET"])
    async def diffpibs_page(self, request):
        raw_conn = engine.raw_connection()
        cursor = None
        try:
            raw_conn.create_function("parse_ipn", 1, parse_ipn)
            cursor = raw_conn.cursor()

            result = raw_conn.execute("""
                SELECT DISTINCT
        NUMIDENT AS ipn,
        TRIM(LN || ' ' || NM || ' ' || FTN) AS pib,
         parse_ipn(NUMIDENT) AS ipndata
    FROM Df1s
    WHERE NUMIDENT IN (
        SELECT NUMIDENT
        FROM Df1s
        GROUP BY NUMIDENT
        HAVING COUNT(
            DISTINCT TRIM(LN || ' ' || NM || ' ' || FTN)
        ) > 1
    )
    ORDER BY NUMIDENT;
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
