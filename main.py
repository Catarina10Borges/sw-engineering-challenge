import logging
from fastapi import FastAPI, HTTPException
from typing import List
from data_base import get_all_bloqs, get_bloq_by_id, get_all_lockers, get_locker_by_id, get_all_rents, get_rent_by_id
from enums import Bloq, Locker, Rent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed")
    return {"message": "Hello Customer! 👋\nWelcome to the Locker API!"}

# my endpoints
# Bloqs
@app.get("/bloqs", response_model=List[Bloq])
def list_bloqs():
    return get_all_bloqs()

@app.get("/bloqs/{bloq_id}", response_model=Bloq)
def get_bloq(bloq_id: str):
    bloq = get_bloq_by_id(bloq_id)
    if bloq is None:
        raise HTTPException(status_code=404, detail="Bloq not found")
    return bloq

# Lockers
@app.get("/lockers", response_model=List[Locker])
def list_lockers():
    return get_all_lockers()

@app.get("/lockers/{locker_id}", response_model=Locker)
def get_locker(locker_id: str):
    locker = get_locker_by_id(locker_id)
    if locker is None:
        raise HTTPException(status_code=404, detail="Locker not found")
    return locker

# Rents
@app.get("/rents", response_model=List[Rent])
def list_rents():
    return get_all_rents()

@app.get("/rents/{rent_id}", response_model=Rent)
def get_rent(rent_id: str):
    rent = get_rent_by_id(rent_id)
    if rent is None:
        raise HTTPException(status_code=404, detail="Rent not found")
    return rent

