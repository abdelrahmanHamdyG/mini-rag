from fastapi import FastAPI, APIRouter, Depends,UploadFile,File,status
from fastapi.responses import JSONResponse
import os

from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from routes import ProcessRequest  
from models import ResponseSignals
from helpers import Logger

logger=Logger().get_logger()


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



@data_router.post("/process/{project_id}")
async def process_file(project_id:str,process_request:ProcessRequest):
    
    
    file_id=process_request.file_id
    chunk_size=process_request.chunck_size
    overlap_size=process_request.overlap_size


    logger.debug(msg=f" project_id {project_id} , file_id {file_id}")

    
    
    
    processController=ProcessController(project_id=project_id)

    file_content= processController.get_file_content(file_id)

    file_chunks=processController.process_file_content(file_content,file_id,chunk_size,overlap_size)

    if file_chunks is None or len(file_chunks)==0: 
        return JSONResponse(
            status_code=400,
            content={
                "signal": ResponseSignals.FILE_PROCESSED_FAILED.value
            }

        )
   
    return file_chunks