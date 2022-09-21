from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.router import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.include_router(router)
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
Base.metadata.create_all(bind=engine)


# uvicorn app.main:app --reload
