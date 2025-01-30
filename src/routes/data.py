from fastapi import FastAPI, APIRouter, Depends,UploadFile,File
import os
from helpers.config import get_settings, Settings



data_router=APIRouter(prefix="/data")

@data_router.post("/upload/{project_id}")
def upload_file(project_id:str,file: UploadFile,app_settings: Settings = Depends(get_settings)):
    return {"message":"Data uploaded successfully"}