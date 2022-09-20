from fastapi import UploadFile, APIRouter, HTTPException, Depends, File
from fastapi_jwt_auth import AuthJWT
from starlette.responses import FileResponse
from app.auth import auth_token
import json
import os


router = APIRouter()


@router.get("/")
def get():
    return {"message": " This is Single Well server. "}


# get site_map
@router.get("/site_map")
def get():
    path = f"{os.getcwd()}/app/site_map.json"
    return FileResponse(path=path)


# get page
@router.get("/page/{language}/{page_name}")
def get(page_name: str, language: str):
    path = f"{os.getcwd()}/app/PageJson/{language}/{page_name}.json"
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="page isn't exist")
    try:
        with open(path) as file:
            page = json.load(file)
        return page
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Get page error")


# create page
@router.post("/page/{language}/{page_name}")
async def upload(page_name: str, language: str, data: dict, authorize: AuthJWT = Depends()):
    # auth_token(authorize)
    path = f"{os.getcwd()}/app/PageJson/{language}/{page_name}.json"
    try:
        with open(path, "w") as file:
            json.dump(data, file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Create error")


# delete page
@router.delete("/page/{language}/{page_name}")
def get(page_name: str, language: str, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = f"{os.getcwd()}/app/PageJson/{language}/{page_name}.json"
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
    path = os.getcwd() + "/app/files/" + filename
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="file isn't exist")
    try:
        return FileResponse(path=path, filename=filename)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Download error")


# upload file
@router.post("/file")
async def upload(Image_file: UploadFile = File(...)):

# async def upload(Image_file: UploadFile = File(...), authorize: AuthJWT = Depends()):
    # auth_token(authorize)
    path = os.getcwd() + "/app/files/" + Image_file.filename
    try:
        with open(path, "wb") as _file:
            file = Image_file.file.read()
            _file.write(file)
        return "upload success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Upload error")


# delete file
@router.delete("/file/{filename}")
def get(filename: str, authorize: AuthJWT = Depends()):
    auth_token(authorize)
    path = os.getcwd() + "/app/files/" + filename
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="file isn't exist")
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Delete error")
