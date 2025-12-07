from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import  engine
from app.database.base import base
from app.routers.auth import auth_router
from app.routers.store import store_router



base.metadata.create_all(bind=engine)

app = FastAPI(
    title="trillmill-BACKEND",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])


app.include_router(store_router, prefix="/api/v1/store", tags=["Store"])


