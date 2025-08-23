from fastapi import FastAPI
from app.routers import users_router
from app.auth import auth_router 
import logging

app = FastAPI(title="Event Booking System")

# Register routers
app.include_router(users_router.router)
app.include_router(auth_router.router, tags=["Auth"])

logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


@app.get("/")
async def root():
    return {"message": "Event Booking System is running 🚀"}
