from fastapi import FastAPI,APIRouter
import os
base_router=APIRouter(prefix="/api/v06",tags=['v06'])
@base_router.get("/")
def welcome():
    appversion=os.getenv('APP_VERSION')
    appname=os.getenv('APP_NAME')
    return{
        'app_name':appname,
        'app_version':appversion,
    }


