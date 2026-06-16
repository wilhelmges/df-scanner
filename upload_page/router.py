import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Визначаємо шлях до локальних шаблонів модуля
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

custom_router = APIRouter(prefix="/my-independent-upload")

@custom_router.get("/", response_class=HTMLResponse)
async def my_custom_page(request: Request):
    # Віддаємо твій чистий HTML-файл
    return templates.TemplateResponse("index.html", {"request": request})
