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
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
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

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html"
    )

def process_file(job_id: str, file_path: Path):
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