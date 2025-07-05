from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_lockers, get_locker_by_id
from enums import Locker

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