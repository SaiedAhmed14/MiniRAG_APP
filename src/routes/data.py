from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import os
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from models import ResponseSignals
import logging
from .schemes.data import ProcessRequest

logger=logging.getLogger("uvicorn.errror")

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
        content={
            "message": result_signal
                }
        )
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path,file_id=data_controller.generate_unique_filepath(orig_file_name=file.filename,project_id=project_id)
    try:
        async with aiofiles.open(file_path, mode='wb') as f:
            while chunk:=await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        # Log error
        logger.error(f"Error while uploading file: {e}")            
        
        # Return error response
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignals.FILE_UPLOADED_FAILED.value
                    }
                ) 
    #RETURN SUCCESS RESPONSE
    return JSONResponse(
        content={
            "signal":ResponseSignals.FILE_UPLOADED_SUCCESS.value,
            "file_id":file_id
            }
        )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):


    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlab_size=process_request.overlap_size


    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)

    
    file_chunks=process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlab_size
    )
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignals.PROCESSING_FAILED.value
                    }
                )
    return file_chunks

