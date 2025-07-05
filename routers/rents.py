# routers/rents.py
from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_rents, get_rent_by_id
from enums import Rent

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
