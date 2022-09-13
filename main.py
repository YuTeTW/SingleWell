from fastapi import FastAPI
from db.database import engine, Base
from api.router import router

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)
