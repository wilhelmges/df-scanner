from sqladmin import BaseView, expose
from starlette.responses import HTMLResponse

class SampleReportView(BaseView):
    name = "sample report"
    category = "Звіти та SQL"

    @expose("/test")
    def index(self, request):
        return HTMLResponse("""
                <h1>TEST</h1>
            """)
