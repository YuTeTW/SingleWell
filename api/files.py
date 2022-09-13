from fastapi import UploadFile, APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from starlette.responses import FileResponse
from auth import auth_token
import json
import os


router = APIRouter()


# get page
@router.get("/page/{pagename}")
async def get(pagename: str):
    path = os.getcwd() + "/Pagejson/" + pagename + ".json"
    if not os.path.isfile(path):
        print(123213)
        raise HTTPException(status_code=400, detail="page isn't exist")
    try:
        with open(path) as file:
            page = json.load(file)
        return page
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Get page error")


# create page
@router.post("/page/{pagename}")
async def upload(pagename: str, data: dict, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = os.getcwd() + "/Pagejson/" + pagename + ".json"
    try:
        with open(path, "w") as file:
            json.dump(data, file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Create error")


@router.delete("/page/{pagename}")
def get(pagename: str, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = os.getcwd() + "/Pagejson/" + pagename + ".json"
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="page isn't exist")
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Delete error")


# download file
@router.get("/file/{filename}")
def get(filename: str):
    path = os.getcwd() + "/AllPic/" + filename
    if not os.path.isfile(path):
        print(123213)
        raise HTTPException(status_code=400, detail="file isn't exist")
    try:
        return FileResponse(path=path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Download error")


# upload file
@router.post("/file")
async def upload(file: UploadFile, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = os.getcwd() + "/AllPic/" + file.filename
    try:
        with open(path, "wb") as _file:
            file = file.file.read()
            _file.write(file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Upload error")


@router.delete("/file/{filename}")
def get(filename: str, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = os.getcwd() + "/AllPic/" + filename
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="file isn't exist")
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Delete error")
