
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from .auth import verify_token
import dbmanager
import sqlite3
import asyncio

app = FastAPI(title="NOC Core API")


class CheckInData(BaseModel):
    device_id: str
    status: str
    time: str


print("loading databases...")

database_name = "devices.db"
database_name2 = "checks.db"

sqlite3.connect(database_name).close()
sqlite3.connect(database_name2).close()

print("Database completed.")


def useless():
    dbmanager.query_dev(database_name,"SELECT * FROM devices")
    #sampler for db manager


# Base alive return (send)
@app.get("/")
def home():
    return {"status": "online"}


# Get all devices (send)
@app.get("/api/v1/devices", dependencies=[Depends(verify_token)])
def devices():
    return {
        "devices": dbmanager.query_dev(
            database_name,
            "SELECT * FROM devices"
        ),
        "authenticated": True
    }


# Return if a specific device is online (send)
@app.get("/api/v1/operation", dependencies=[Depends(verify_token)])
def operation(device):
    working = dbmanager.query_dev(
        database_name,
        "SELECT * FROM devices"
    )

    return {"devices": working}


# Device checkin (receive)
@app.post("/api/v1/check_in", dependencies=[Depends(verify_token)])
def check_in(data: CheckInData):
    dbmanager.query_dev(
        database_name2,
        "INSERT INTO check_in (device_id, status, time) VALUES (?, ?, ?)",
        (data.device_id, data.status, data.time)
    )

    print(f"Status: {data.status}")
    print(f"Client Time: {data.time}")

    return {"received": True}


# Device checkup and alert (internal)
async def inactive_check():
    devices = dbmanager.query_dev(
        database_name,
        "SELECT * FROM devices WHERE status = ?",
        ("inactive",)
    )

    for device in devices:
        print(f"Device {device[0]} isn't responding. Please check on it!")

    await asyncio.sleep(60)
