from fastapi import FastAPI,APIRouter,Depends
from helpers.config import get_settings,Settings
import os
base_router=APIRouter(prefix="/api/v07",tags=['v07'])
@base_router.get("/")
async def welcome(app_settings:Settings=Depends(get_settings)):
    app_settings=get_settings()
    appname=app_settings.APP_NAME
    appversion=app_settings.APP_VERSION
    return{
        'app_name':appname,
        'app_version':appversion,
    }


