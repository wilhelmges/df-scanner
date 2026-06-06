from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose
from core import check_tax_code, parse_ipn


class Process_updates(BaseView):
    icon = "fa-solid fa"
    category = 'Обслуговування БД'

    name = "Оновлення БД"

    @expose("/getupdates", methods=["GET"])
    async def getupdates(self, request):
        raw_conn = engine.raw_connection()
        cursor = None
        try:
            cursor = raw_conn.cursor()


        finally:
            cursor.close()
            raw_conn.close()

        return await self.templates.TemplateResponse(request, "getupdates.html", {
            "rows": []
        })
