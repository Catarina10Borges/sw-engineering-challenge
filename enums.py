#Each bloq contains many lockers (doors)
#Each Locker contain a Rent (parcel)

from pydantic import BaseModel
from enum import Enum
from typing import Optional

class RentStatus(str, Enum):
    CREATED = "CREATED"
    WAITING_DROPOFF = "WAITING_DROPOFF"
    WAITING_PICKUP = "WAITING_PICKUP"
    DELIVERED = "DELIVERED"

class RentSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

class LockerStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class Bloq(BaseModel):
    id: str
    title: str
    address: str

class Locker(BaseModel):
    id: str
    bloqId: str
    status: LockerStatus
    isOccupied: bool

class Rent(BaseModel):
    id: str
    lockerId: Optional[str]
    weight: float
    size: RentSize
    status: RentStatus
