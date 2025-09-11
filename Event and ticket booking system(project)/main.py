from fastapi import FastAPI

from app.routers import users_router
from app.routers import admin_router
from app.routers import event_router
from app.routers import venue_router
from app.routers import booking_router

from app.auth import auth_router

import logging

app = FastAPI(title="Event Booking System")

# Register routers
app.include_router(users_router.router)
app.include_router(auth_router.router, tags=["auth"])
app.include_router(admin_router.router)
app.include_router(auth_router.router)
app.include_router(event_router.router)
app.include_router(venue_router.router)
app.include_router(booking_router.router)


logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


@app.get("/")
async def root():
    return {"message": "Event Booking System is running 🚀"}
