from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

#* FastAPI app initialization
app=FastAPI()


#& setting up the database client
@app.on_event("startup")
async def startup_db_client():
    settings=get_settings()
    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]

#& shutting down the database client
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(base.base_router)
app.include_router(data.data_router)