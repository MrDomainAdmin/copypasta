"""Copypasta Main"""
import os
import uvicorn
import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from modules.router import createRouter
from modules.variables import STATICFILESPATH, DATABASE, HOST, PORT


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["default"]["use_colors"] = False
log_config["formatters"]["access"]["use_colors"] = False

# Init DB
with sqlite3.connect(DATABASE) as conn:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS hashes
                      (filename TEXT PRIMARY KEY, md5 TEXT)"""
    )

# Include the router in your app
app.include_router(createRouter(app))


if __name__ == "__main__":
    if not os.path.exists(STATICFILESPATH):
        os.mkdir(STATICFILESPATH)
    with open("./static/clipboard", 'w'):
        pass
    uvicorn.run(app, host=HOST, port=PORT, log_config=log_config)
