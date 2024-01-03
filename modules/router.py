from fastapi import (
    Request,
    Form,
    BackgroundTasks,
)
from fastapi.responses import RedirectResponse
from fastapi import APIRouter
from modules.util import (
    b64,
    preview,
    rm,
    shortcut,
    upload,
    uploadText,
    indexPost,
    indexGet,
)


def createRouter(app):
    router = APIRouter()

    @router.get("/b64/{file:path}", tags=["text"])
    def view_b64(file: str):
        return b64(file)

    @router.post("/text", tags=["text"])
    async def add_text(request: Request):
        await uploadText(request)
        return RedirectResponse(url="/", status_code=303)

    @router.get("/preview/{file:path}", tags=["file"])
    def preview_file(file: str):
        return preview(file)

    @router.get("/{fileIndex:int}", tags=["file"])
    def download_shortcut(fileIndex: int):
        print("getindexdownload")
        return shortcut(fileIndex)

    @router.post("/upload", tags=["file"])
    async def upload_file(request: Request):
        return await upload(request)

    @router.post("/remove", tags=["file"])
    async def remove(backgroundTasks: BackgroundTasks,
                     filedel: list = Form(None)):
        return await rm(backgroundTasks, filedel)

    @router.get("/")
    async def index_get(request: Request):
        print("/get")
        return indexGet(request)

    @router.post("/")
    async def index_post(request: Request):
        print("/post")
        return await indexPost(request)

    return router
