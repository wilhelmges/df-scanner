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
