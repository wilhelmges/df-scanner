import hashlib
import uuid
from pathlib import Path
from threading import Lock

from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from admin.auth import AdminAuth
from admin.ipn_withdiffpibs import IpnWithDiffPibs
from admin.notvalid_ipns import NotvalidIpns
from admin.pib_withdifferent_ipns import PibWithDifferetIpns
from admin.views import Df1Admin, Df4Admin, Df5Admin
from db import engine
from grab import process_df
from imports_repository import add_file, file_processed

# Import models before admin setup.
from models.dbf110 import Df1
from models.dbf410 import Df4
from models.dbf510 import Df5

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

def process_file(job_id: str, file_path: Path,file_hash, adjustment=True):
    """
    Імітація довгої обробки файлу.
    """
    print('in processing ', adjustment)
    try:
        with jobs_lock:
            jobs[job_id]["status"] = "processing"
            jobs[job_id]["progress"] = 0

        process_df(file_path, adjustment)
        add_file(file_hash, str(file_path), "done")

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
    filetype: bool = Form(...)
):
    original_name = file.filename or "unknown"
    if not original_name.lower().endswith(".dbf"):
        raise HTTPException(
            status_code=400,
            detail="Дозволені лише файли .dbf"
        )

    print('adjustment ',filetype)

    file_uuid = uuid.uuid4()
    stored_name = f"{original_name}"

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
                        status_code=409,
                        detail="Файл занадто великий"
                    )

                sha256.update(chunk)
                f.write(chunk)

        file_hash = sha256.hexdigest()
        job_id = str(uuid.uuid4())

        if file_processed(file_hash):
            return {
                "status": "already_processed",
                "message": "Файл вже був оброблений",
                "processing_status": 'done'
            }

        with jobs_lock:
            jobs[job_id] = {
                "status": "queued",
                "progress": 0,
                "error": None
            }

        background_tasks.add_task(
            process_file,
            job_id,
            file_path,
            file_hash,
            filetype
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

@app.get("/debug")
def health_check():
    return {"status": "ok"}
