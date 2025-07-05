from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_lockers, get_locker_by_id, update_locker
from enums import Locker, LockerStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/lockers", response_model=List[Locker])
def list_lockers():
    return get_all_lockers()

@router.get("/lockers/{locker_id}", response_model=Locker)
def get_locker(locker_id: str):
    locker = get_locker_by_id(locker_id)
    if locker is None:
        raise HTTPException(status_code=404, detail="Locker not found")
    return locker

# To simulate the opening and closing of a locker:
@router.post("/{locker_id}/open")
def open_locker(locker_id: str):
    locker = get_locker_by_id(locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    if locker.status == LockerStatus.OPEN:
        raise HTTPException(status_code=400, detail="Locker already open")

    locker.status = LockerStatus.OPEN
    logging.info("changed locker status to: %s", locker.status)
    update_locker(locker)

    return {"message": f"Locker {locker_id} is now open."}


@router.post("/{locker_id}/close")
def close_locker(locker_id: str):
    locker = get_locker_by_id(locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    if locker.status == LockerStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Locker already closed")

    locker.status = LockerStatus.CLOSED
    logging.info("changed locker status to: %s", locker.status)
    update_locker(locker)

    return {"message": f"Locker {locker_id} is now closed."}