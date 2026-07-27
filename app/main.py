from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import  engine
from app.database.base import base
from app.routers.auth import auth_router
from app.routers.store import store_router
from app.routers.products import product_router
from app.routers.users import user_router
from app.routers.categories import category_router
from app.routers.cart import cart_router
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
  for _ in range(5):
    conn = engine.connect()
    conn.close()

  yield

  engine.dispose()


  



app = FastAPI(
    title="trillmill-BACKEND",
    version="1.0.0",
    lifespan=lifespan
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


app.include_router(product_router, prefix="/api/v1/product", tags=["product"])


app.include_router(user_router, prefix="/api/v1/product", tags=["user"])

app.include_router(category_router,prefix="/api/v1/category", tags=["category"])

app.include_router(cart_router,prefix="/api/v1/cart", tags=["cart"])