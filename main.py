from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse

from sqladmin import Admin, ModelView
from db import engine
from sqlalchemy import text
from sqladmin import BaseView, expose
# імпорт моделей ОБОВ'ЯЗКОВИЙ
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5
from admin.auth import AdminAuth
from starlette.middleware.sessions import SessionMiddleware

from admin.views import Df1Admin, Df4Admin, Df5Admin

from admin.notvalid_ipns import NotvalidIpns
from admin.pib_withdifferent_ipns import PibWithDifferetIpns
from admin.ipn_withdiffpibs import IpnWithDiffPibs
from admin.getupdates import Get_updates
from admin.sample_view import SampleReportView

from fastapi.staticfiles import StaticFiles 
from sqladmin import BaseView, expose
from fastapi.responses import RedirectResponse

from pathlib import Path
import hashlib
import uuid
import time
from threading import Lock

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    BackgroundTasks,
    Request,
    Form
)

from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # після app = FastAPI()
templates = Jinja2Templates(directory="templates")

authentication_backend = AdminAuth(
    #SessionMiddleware,
    secret_key="FES_SECURITY_KEY"
)
admin = Admin(app, engine, authentication_backend=authentication_backend,)

admin.add_view(Df1Admin)
admin.add_view(Df4Admin)
admin.add_view(Df5Admin)

admin.add_view(NotvalidIpns)
admin.add_view(PibWithDifferetIpns)
admin.add_view(IpnWithDiffPibs)

#admin.add_view(SampleReportView)

@app.get("/")
async def root():
    return RedirectResponse(url="/admin")

@app.get("/up42")
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={}
    )

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# Для демо. У реальному проєкті краще БД.
jobs = {}
jobs_lock = Lock()

# ----------------------------
# Upload page
# ----------------------------

@app.get("/getupdates", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html"
    )

def process_file(job_id: str, file_path: Path, adjustment=True):
    """
    Імітація довгої обробки файлу.
    """

    try:
        with jobs_lock:
            jobs[job_id]["status"] = "processing"
            jobs[job_id]["progress"] = 0

        # Імітація 2 хвилин роботи
        for step in range(12):
            time.sleep(0.1)#10

            with jobs_lock:
                jobs[job_id]["progress"] = (step + 1) * 100 // 12

        with jobs_lock:
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["progress"] = 100

    except Exception as exc:
        with jobs_lock:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(exc)

@app.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    filetype: str = Form(...)
):
    original_name = file.filename or "unknown"
    print('adjustment ',filetype)

    file_uuid = uuid.uuid4()
    stored_name = f"{file_uuid}_{original_name}"

    file_path = UPLOAD_DIR / stored_name

    sha256 = hashlib.sha256()
    total_size = 0

    try:
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    f.close()
                    file_path.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=413,
                        detail="Файл занадто великий"
                    )

                sha256.update(chunk)
                f.write(chunk)

        file_hash = sha256.hexdigest()

        job_id = str(uuid.uuid4())

        with jobs_lock:
            jobs[job_id] = {
                "status": "queued",
                "progress": 0,
                "sha256": file_hash,
                "file": stored_name,
            }

        background_tasks.add_task(
            process_file,
            job_id,
            file_path
        )

        return {
            "job_id": job_id,
            "status": "queued",
        }

    finally:
        await file.close()

@app.get("/status/{job_id}")
async def get_status(job_id: str):

    with jobs_lock:
        job = jobs.get(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job