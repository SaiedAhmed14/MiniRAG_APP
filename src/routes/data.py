from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import os
from controllers import DataController,ProjectController
import aiofiles
from models import ResponseSignals
import logging

logger=logging.grtLogger("uvicorn.errror")

data_router=APIRouter(
    prefix="/api/v07/data"
    ,tags=["data","v07"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:Settings=Depends(get_settings)):
    # Validate uploaded file
    data_controller=DataController()
    is_valid, result_signal=data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": result_signal})
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path=data_controller.generate_unique_filepath(orig_file_name=file.filename,project_id=project_id)
    try:
        async with aiofiles.open(file_path, mode='wb') as f:
            while chunk:=await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")            
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal":ResponseSignals.FILE_UPLOADED_FAILED.value}) 
    
    return JSONResponse(content={"signal":ResponseSignals.FILE_UPLOADED_SUCCESS.value})