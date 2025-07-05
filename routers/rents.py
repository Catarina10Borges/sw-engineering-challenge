# routers/rents.py
from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_rents, get_rent_by_id, update_locker, update_rent, get_locker_by_id
from enums import Rent, RentStatus, LockerStatus
import logging
import json
from pathlib import Path
from fastapi import Body
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

class DropoffRequest(BaseModel):
    lockerId: str

# Rents
@router.get("/rents", response_model=List[Rent])
def list_rents():
    return get_all_rents()

@router.get("/rents/{rent_id}", response_model=Rent)
def get_rent(rent_id: str):
    rent = get_rent_by_id(rent_id)
    if rent is None:
        raise HTTPException(status_code=404, detail="Rent not found")
    return rent


# post
@router.put("/{rent_id}/dropoff")
def dropoff_parcel(rent_id: str, payload: DropoffRequest):
    rent = get_rent_by_id(rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")

    if rent.status != RentStatus.WAITING_DROPOFF:
        raise HTTPException(status_code=400, detail="Parcel is not waiting for drop-off")

    locker = get_locker_by_id(payload.lockerId)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    if locker.status != LockerStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Locker is not closed")

    if locker.isOccupied:
        raise HTTPException(status_code=400, detail="Locker is already occupied")

    # Link the locker to the rent
    rent.lockerId = payload.lockerId
    locker.isOccupied = True
    locker.status = LockerStatus.CLOSED
    update_locker(locker)

    rent.status = RentStatus.WAITING_PICKUP
    update_rent(rent)

    return {"message": f"Parcel {rent_id} was dropped off successfully."}

@router.post("/{rent_id}/pickup")
def pickup_parcel(rent_id: str):
    rent = get_rent_by_id(rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")

    if rent.status != RentStatus.WAITING_PICKUP:
        raise HTTPException(status_code=400, detail="Parcel is not waiting for pickup")

    locker = get_locker_by_id(rent.lockerId)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    if locker.status != LockerStatus.OPEN:
        raise HTTPException(status_code=400, detail="Locker is not open")

    if not locker.isOccupied:
        raise HTTPException(status_code=400, detail="Locker is already empty")

    # update locker
    locker.isOccupied = False
    locker.status = LockerStatus.CLOSED
    update_locker(locker)

    # Update rent
    rent.status = RentStatus.DELIVERED
    update_rent(rent)

    return {"message": f"Parcel {rent_id} was picked up successfully."}

#create a new rent:
DATA_DIR = Path(__file__).parent.parent / "data"
RENTS_FILE = DATA_DIR / "rents.json"

def save_rents(rents: List[Rent]):
    with open(RENTS_FILE, "w") as f:
        json.dump([r.model_dump() for r in rents], f, indent=2)

@router.post("/addrent", response_model=Rent)
def create_rent(rent: Rent):
    # check if this id already exists
    if get_rent_by_id(rent.id):
        raise HTTPException(status_code=400, detail="Rent with this ID already exists.")

    # checks if lokcerId exists
    if rent.lockerId and not get_locker_by_id(rent.lockerId):
        raise HTTPException(status_code=400, detail="Locker ID not found.")

    # checks the status
    if rent.status != RentStatus.CREATED:
        raise HTTPException(status_code=400, detail="Status must be CREATED on creation.")

    # save the new rent
    rents = get_all_rents()
    rents.append(rent)
    save_rents(rents)

    logger.info(f"New rent created: {rent.id}")
    return rent

# endpoint to update rent 
@router.put("/update_rent_status", response_model=Rent)
def update_rent_status(
    rent_id: str = Body(...),
    status: RentStatus = Body(...),
    lockerId: str = Body(None)
):
    rent = get_rent_by_id(rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")

    if status == RentStatus.WAITING_DROPOFF:
        if rent.status != RentStatus.CREATED:
            raise HTTPException(status_code=400, detail="Can only move to WAITING_DROPOFF from CREATED")
        rent.status = RentStatus.WAITING_DROPOFF

    elif status == RentStatus.WAITING_PICKUP:
        if rent.status != RentStatus.WAITING_DROPOFF:
            raise HTTPException(status_code=400, detail="Can only move to WAITING_PICKUP from WAITING_DROPOFF")
        if not lockerId:
            raise HTTPException(status_code=400, detail="LockerId required to move to WAITING_PICKUP")

        locker = get_locker_by_id(lockerId)
        if not locker:
            raise HTTPException(status_code=404, detail="Locker not found")

        rent.lockerId = lockerId
        rent.status = RentStatus.WAITING_PICKUP

    else:
        raise HTTPException(status_code=400, detail="Invalid status transition")

    update_rent(rent)
    return rent