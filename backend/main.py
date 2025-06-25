from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import models
from backend.api import affiliate_router, finds_router, suppliers_router, users_router, payments_router
from backend.config import get_settings
from backend.database import engine
from backend.api.auth import router as auth_router


# To create tables at startup with the async engine:
# async with engine.begin() as conn:
#     await conn.run_sync(models.Base.metadata.create_all)

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(affiliate_router)
app.include_router(suppliers_router)
app.include_router(finds_router)
app.include_router(payments_router)
