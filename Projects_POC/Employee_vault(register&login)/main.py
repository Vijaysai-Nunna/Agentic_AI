from fastapi import FastAPI
from app.routers import user_router
from app.utils.logger import setup_logger

app = FastAPI()
app.include_router(user_router.router)
setup_logger()