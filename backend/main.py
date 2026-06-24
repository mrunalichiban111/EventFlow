from fastapi import FastAPI

from app.database.database import engine
from app.database.models import Base

from app.routes.events import router as event_router
from app.routes.users import router as user_router
from app.routes.registrations import (
    router as registration_router
)
from app.routes.auth import router as auth_router
from app.routes.me import router as me_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(event_router)
app.include_router(user_router)
app.include_router(registration_router)
app.include_router(auth_router)
app.include_router(me_router)

@app.get("/")
def home():
    return {"message":"EventFlow AI Backend Running"}