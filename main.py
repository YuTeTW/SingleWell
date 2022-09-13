import json
import os

from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse

app = FastAPI()




@app.get("/page/{pagename}")
async def get(pagename: str):
    try:
        with open(os.getcwd() + "/Pagejson/" + pagename + ".json") as file:
            page = json.load(file)
        return page
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="error")


@app.post("/page/{pagename}")
async def upload(pagename: str, data: dict):
    try:
        with open(os.getcwd() + "/Pagejson/" + pagename + ".json", "w") as file:
            json.dump(data, file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")


# download file
@app.get("/file/{filename}")
def get(filename: str):
    try:
        path = os.getcwd() + "/AllPic/" + filename
        return FileResponse(path=path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")


# upload file
@app.post("/file")
async def upload(file: UploadFile):
    try:
        path = os.getcwd() + "/AllPic/" + file.filename
        with open(path, "wb") as _file:
            file = file.file.read()
            _file.write(file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")
