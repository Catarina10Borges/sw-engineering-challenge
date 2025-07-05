# routers/rents.py
from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_rents, get_rent_by_id, update_locker, update_rent, get_locker_by_id
from enums import Rent, RentStatus, LockerStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
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
@router.post("/{rent_id}/dropoff")
def dropoff_parcel(rent_id: str):
    rent = get_rent_by_id(rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")

    if rent.status != RentStatus.WAITING_DROPOFF:
        raise HTTPException(status_code=400, detail="Parcel is not waiting for drop-off")

    locker = router.get_locker_by_id(rent.lockerId)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    if locker.status != LockerStatus.OPEN:
        raise HTTPException(status_code=400, detail="Locker is not open")

    if locker.isOccupied:
        raise HTTPException(status_code=400, detail="Locker is already occupied")

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