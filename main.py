import logging
from fastapi import FastAPI, HTTPException
from typing import List
from data_base import get_all_bloqs, get_bloq_by_id, get_all_lockers, get_locker_by_id, get_all_rents, get_rent_by_id
from routers import bloqs, lockers, rents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed")
    return {"message": "Hello Customer! 👋\nWelcome to the Locker API!"}

app.include_router(bloqs.router)
app.include_router(lockers.router)
app.include_router(rents.router)

