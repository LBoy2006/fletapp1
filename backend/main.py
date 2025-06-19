from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .api import affiliate_router, finds_router, suppliers_router, users_router
from .config import get_settings
from .database import engine

models.Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(affiliate_router)
app.include_router(suppliers_router)
app.include_router(finds_router)
