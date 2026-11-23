from fastapi import FastAPI, Depends
from .auth import verify_token
import sqlite3

app = FastAPI(title="NOC Core API")

print("loading database...")
database_name = "devices.db"

connection = sqlite3.connect(database_name)

print("Database completed.")

connection.close()
def query(sql, params=()):
    with sqlite3.connect("devices.db") as db:
        cursor = db.execute(sql, params)

        if cursor.description:
            return cursor.fetchall()

        return cursor.rowcount
    
@app.get("/")
def home():
    return {"status": "online"}

@app.get("/api/v1/devices", dependencies=[Depends(verify_token)])
def devices():
    return {
        "devices": query("SELECT * FROM devices"),
        "authenticated": True
    }
