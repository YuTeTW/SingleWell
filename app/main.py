from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.router import router

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)


# uvicorn app.main:app --reload
