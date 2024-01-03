import base64
import mimetypes
from datetime import datetime
from hashlib import md5
from math import ceil
import os
from pathlib import Path
import sqlite3
import shutil
import threading
from fastapi import (
    Request,
    Form,
    BackgroundTasks,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response, FileResponse
from starlette.responses import PlainTextResponse
from modules.variables import STATICFILESPATH, DATABASE


def getHome(request):
    downloads = getFileList()
    host = request.base_url
    clipboard = getClipboard()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "host": host, "downloads": downloads, "clipboard": clipboard}
    )


def setMd5(filename, md5Hash):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO hashes (filename, md5) VALUES (?, ?)",
            (filename, md5Hash),
        )


def getMd5(filename):
    with sqlite3.connect(DATABASE) as conn:
        row = conn.execute(
            "SELECT md5 FROM hashes WHERE filename=?", (filename,)
        ).fetchone()
        return row[0] if row else None


def getClipboard():
    return open("./static/clipboard", "r").read()

# FastAPI Templates
templates = Jinja2Templates(directory="templates")

# Routes and Logic


def getUploadMd5(file):
    path = STATICFILESPATH + file
    size = os.stat(path).st_size

    if size >= 2 * 1024 * 1024 * 1024:
        size = str(ceil(size / (1024 * 1024 * 1024))) + "GB"
        md5Sum = "File too large"
    elif size >= 1024 * 1024 * 1024:
        size = str(ceil(size / (1024 * 1024 * 1024))) + "GB"
        md5Sum = getMd5(file)
        if not md5Sum:
            md5Sum = md5(open(path, "rb").read()).hexdigest()
            setMd5(file, md5Sum)
    elif size > 1048576:
        size = str(ceil(size / 1048576)) + "MB"
        md5Sum = getMd5(file)
        if not md5Sum:
            md5Sum = md5(open(path, "rb").read()).hexdigest()
            setMd5(file, md5Sum)
    elif 1048576 > size > 1024:
        size = str(ceil(size / 1024)) + "KB"
        md5Sum = getMd5(file)
        if not md5Sum:
            md5Sum = md5(open(path, "rb").read()).hexdigest()
            setMd5(file, md5Sum)
    else:
        size = str(size) + "B"
        md5Sum = getMd5(file)
        if not md5Sum:
            md5Sum = md5(open(path, "rb").read()).hexdigest()


def getFileList():
    staticFiles = []
    for file in os.listdir(STATICFILESPATH):
        path = STATICFILESPATH + file
        size = os.stat(path).st_size

        if size >= 2 * 1024 * 1024 * 1024:
            size = str(ceil(size / (1024 * 1024 * 1024))) + "GB"
            md5Sum = "File too large"
        elif size >= 1024 * 1024 * 1024:
            size = str(ceil(size / (1024 * 1024 * 1024))) + "GB"
            md5Sum = getMd5(file)
            if not md5Sum:
                md5Sum = md5(open(path, "rb").read()).hexdigest()
                setMd5(file, md5Sum)
        elif size > 1048576:
            size = str(ceil(size / 1048576)) + "MB"
            md5Sum = getMd5(file)
            if not md5Sum:
                md5Sum = md5(open(path, "rb").read()).hexdigest()
                setMd5(file, md5Sum)
        elif 1048576 > size > 1024:
            size = str(ceil(size / 1024)) + "KB"
            md5Sum = getMd5(file)
            if not md5Sum:
                md5Sum = md5(open(path, "rb").read()).hexdigest()
                setMd5(file, md5Sum)
        else:
            size = str(size) + "B"
            md5Sum = getMd5(file)
            if not md5Sum:
                md5Sum = md5(open(path, "rb").read()).hexdigest()

        cTime = datetime.fromtimestamp(os.stat(path).st_ctime).strftime(
            "%d %b %Y %H:%M:%S"
        )
        staticFiles.append([file, path, size, cTime, md5Sum])
    staticFiles.sort(
        key=lambda item: datetime.strptime(item[3], "%d %b %Y %H:%M:%S"),
        reverse=True
    )

    return staticFiles


def deleteHash(file):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM hashes WHERE filename=?", (file,))

# ------------------- Route Logic -------------------


# /b64/file
def b64(file: str):
    if file in os.listdir(STATICFILESPATH):
        with open(STATICFILESPATH + file, "rb") as f:
            data = f.read()
            b64Data = base64.b64encode(data)
        return b64Data
    else:
        return {"message": "File not found"}


# /text
async def uploadText(request: Request):
    form = await request.form()
    if "save_b64" in form and "text" in form:
        text = form.get("text").encode()
        if text:
            filename = datetime.now().strftime("%d%b%Y_%H%M%S.b64.txt")
            data = base64.b64encode(text)
            data = data.decode("utf-8")
            with open(STATICFILESPATH + filename, "w") as f:
                f.write(data)
    elif "text" in form:
        text = form.get("text")
        if text:
            filename = datetime.now().strftime("%d%b%Y_%H%M%S.txt")
            with open(STATICFILESPATH + filename, "w") as f:
                f.write(text)

    return getHome(request)


# /clipboard
async def saveClipboard(request: Request):
    form = await request.form()
    text = form.get("clipboard")
    filepath = "./static/clipboard"
    if text:
        with open(filepath, "w") as f:
            f.write(text)
    else:
        with open(filepath, "w") as f:
            pass
    return getHome(request)




# /preview
def preview(file: str):
    file_path = f"{STATICFILESPATH}{file}"

    # Check if the file exists
    if not os.path.exists(file_path):
        return {"message": "File not found"}

    # Guess the MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and (
        "script" in mime_type or "text" in mime_type or "x-sh" in mime_type
    ):
        mime_type = "text/plain"
    else:
        mime_type = mime_type or "text/plain"
    mime_type = "text/plain"
    with open(file_path, "rb") as f:
        data = f.read()

    # Serve the file with appropriate content type
    return Response(content=data, media_type=mime_type)


# /remove
async def rm(backgroundTasks: BackgroundTasks, filedel: list = Form(None)):
    if not filedel:
        return RedirectResponse(url="/", status_code=303)

    for file in filedel:
        try:
            if os.path.exists(STATICFILESPATH + file):
                os.remove(STATICFILESPATH + file)
                backgroundTasks.add_task(deleteHash, file)
        except Exception as e:
            print(f"error deleting {file}: {e}")
    return RedirectResponse(url="/", status_code=303)


# /<int>
def shortcut(fileIndex: int):
    files = getFileList()
    if 1 <= fileIndex <= len(files):
        file_name = files[fileIndex - 1][0]
        file_path = os.path.join(STATICFILESPATH, file_name)

        if os.path.exists(file_path):
            return FileResponse(file_path)

    return Response(status_code=204)


# /upload
async def upload(request: Request):
    form = await request.form()
    print(form)
    uploadedFiles = form.getlist("file")

    def uploader(file, destination):
        if file:
            with open(destination, "w+b") as file:
                shutil.copyfileobj(uploadedFile.file, file)

    threads = []
    for uploadedFile in uploadedFiles:
        thread = threading.Thread(
            target=uploader,
            args=(uploadedFile,
                  Path(STATICFILESPATH).joinpath(uploadedFile.filename)),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    userAgent = request.headers.get("user-agent", "")
    if "curl" in userAgent.lower():
        return PlainTextResponse(content="complete\n")
    return getHome(request)


# / [post]
async def indexPost(request: Request):
    return getHome(request)


# / [get]
def indexGet(request: Request):
    return getHome(request)
