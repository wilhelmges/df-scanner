from sqlalchemy import text
from starlette.responses import HTMLResponse
from sqladmin import BaseView, expose

from db import engine

class SampleReportView(BaseView):
    name = "sample report"
    category = "Звіти та SQL"

    @expose("/test")
    def index(self, request):
        return HTMLResponse("""
                <h1>TEST</h1>
            """)