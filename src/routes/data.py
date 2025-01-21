from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import os
from controllers import DataController,ProjectController


data_router=APIRouter(
    prefix="/api/v07/data"
    ,tags=["data","v07"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:Settings=Depends(get_settings)):
    # Validate uploaded file
    is_valid, result_signal=DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": result_signal})
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    