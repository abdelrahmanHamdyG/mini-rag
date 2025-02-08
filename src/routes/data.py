from fastapi import FastAPI, APIRouter, Depends,UploadFile,File,status
from fastapi.responses import JSONResponse
import os

from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController
import aiofiles
from models import ResponseSignals
import logging

logger=logging.getLogger("uvicorn.error")


data_router=APIRouter(prefix="/data")

@data_router.post("/upload/{project_id}")
async def upload_file(project_id:str,file: UploadFile= File(None),app_settings: Settings = Depends(get_settings)):
    
    
    is_valid,signal_message=DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=400,
            content={"message": signal_message}
        )
    
    project_dir_path= ProjectController().get_project_path(project_id=project_id)


    file_path=os.path.join(project_dir_path,file.filename)

    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:=await file.read(5120000):
                await f.write(chunk)    
    except Exception as e:
        logger.error(f"error while uploading file: {e}")
        return JSONResponse(
            status_code=400,
            content={"message": ResponseSignals.FILE_UPLOADED_FAILED.value}
        )


    return JSONResponse(
            content={"message": ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value }
        )



