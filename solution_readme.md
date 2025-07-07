# Rent & Locker API

This project simulates the workflow for rent's drop-off and pickup in automated lockers.
The API is built with **FASTAPI**, using REST endpoints organized in `routers/rents.py`and `routers/lockers.py`.

---
## Overview

### MAin Entities:
- **Rent**: Represents the rental agreement for a locker for a parcel.
- **Locker**: Represents the physical locker where the parcel will be stored.

---
## Workflow
Below is the complete cycle **from creating a rent to picking up the parcel**, with the **endpoints** used at each step.

---
## 1 - Create a new rent
Create a new rent record with status `CREATED`.

**Endpoint:**
POST/addrent

**Example Body:**
{
  "id": "50be06a8-1dec-4b18-a23c-e98588207754",
  "lockerId": null,
  "weight": 5.0,
  "size": "M",
  "status": "CREATED"
}

---
## 2 - Rent is ready to dropoff
**Endpoint:**
PUT/update_rent_status

**Example Body:**
{
  "rent_id": "50be06a8-1dec-4b18-a23c-e98588207754",
  "status": "WAITING_DROPOFF"
}

---
## 3 - Drop off the rent
Links the locker to the rent, marks the locker as occupied and changes the rent status to "WATING_PICKUP"

**Endpoint:**
PUT/{rent_id}/dropoff

**Example Body:**
{
  "lockerId": "LOCKER123"
}

The lockerId could be one that is not occupied or one new locker.

---
## 4 - Open the locker for pickup
Simulates the customer opening the locker to pick up the rent.

**Endpoint:**
POST/{locker_id}/open

---
## 5 - Pick up the rent
Completes the process: frees up the locker and marks the rent as DELIVERED.


---
✔️ Locker is automatically freed up on pickup:

The pickup endpoint sets locker.isOccupied = False and locker.status = CLOSED.

✔️ While the rent is not DELIVERED, the locker remains occupied.
---

To execute the API use the command:
>> uvicorn main:app --reload