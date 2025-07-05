import json
from pathlib import Path
from typing import List, Optional
from enums import Bloq, Locker, Rent
import logging

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"

def load_json(file_name):
    with open(DATA_DIR / file_name, "r") as f:
        return json.load(f)

def save_json(file_name, data):
    with open(DATA_DIR / file_name, "w") as f:
        json.dump(data, f, indent=2)

def get_all_bloqs() -> List[Bloq]:
    data = load_json("bloqs.json")
    return [Bloq(**item) for item in data]

def get_bloq_by_id(bloq_id: str) -> Optional[Bloq]:
    bloqs = get_all_bloqs()
    for bloq in bloqs:
        if bloq.id == bloq_id:
            return bloq
    return None

def get_all_lockers() -> List[Locker]:
    data = load_json("lockers.json")
    return [Locker(**item) for item in data]

def get_locker_by_id(locker_id: str) -> Optional[Locker]:
    lockers = get_all_lockers()
    for locker in lockers:
        if locker.id == locker_id:
            return locker
    return None

def get_all_rents() -> List[Rent]:
    data = load_json("rents.json")
    return [Rent(**item) for item in data]

def get_rent_by_id(rent_id: str) -> Optional[Rent]:
    rents = get_all_rents()
    for rent in rents:
        if rent.id == rent_id:
            return rent
    return None

# change rents and locker:
# Update locker
def update_locker(updated_locker: Locker):
    lockers = get_all_lockers() 
    for idx, locker in enumerate(lockers):
        if locker.id == updated_locker.id:
            lockers[idx] = updated_locker 
            break
    save_json("lockers.json", [locker.model_dump() for locker in lockers])

# Update rent
def update_rent(updated_rent: Rent):
    rents = get_all_rents()
    for idx, rent in enumerate(rents):
        if rent.id == updated_rent.id:
            rents[idx] = updated_rent
            break
    save_json("rents.json", [rent.model_dump() for rent in rents])