# routers/bloqs.py
from fastapi import APIRouter, HTTPException
from typing import List
from data_base import get_all_bloqs, get_bloq_by_id
from enums import Bloq

router = APIRouter()

# Bloqs
@router.get("/bloqs", response_model=List[Bloq])
def list_bloqs():
    return get_all_bloqs()

@router.get("/bloqs/{bloq_id}", response_model=Bloq)
def get_bloq(bloq_id: str):
    bloq = get_bloq_by_id(bloq_id)
    if bloq is None:
        raise HTTPException(status_code=404, detail="Bloq not found")
    return bloq