from fastapi import UploadFile, APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from starlette.responses import FileResponse
import json
import os

from auth import auth_token

router = APIRouter()


@router.get("/page/{pagename}")
async def get(pagename: str):
    try:
        with open(os.getcwd() + "/Pagejson/" + pagename + ".json") as file:
            page = json.load(file)
        return page
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")


@router.post("/page/{pagename}")
async def upload(pagename: str, data: dict, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    try:
        with open(os.getcwd() + "/Pagejson/" + pagename + ".json", "w") as file:
            json.dump(data, file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")


# download file
@router.get("/file/{filename}")
def get(filename: str):
    try:
        path = os.getcwd() + "/AllPic/" + filename
        return FileResponse(path=path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")


# upload file
@router.post("/file")
async def upload(file: UploadFile, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    try:
        path = os.getcwd() + "/AllPic/" + file.filename
        with open(path, "wb") as _file:
            file = file.file.read()
            _file.write(file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error")





