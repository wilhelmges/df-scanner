from sqladmin import BaseView, expose

from db import engine


class Get_updates(BaseView):
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
