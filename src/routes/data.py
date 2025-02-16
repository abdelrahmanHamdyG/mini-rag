from fastapi import FastAPI, APIRouter, Depends,UploadFile,File,status,Request
from fastapi.responses import JSONResponse
import os

from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from routes import ProcessRequest  
from models import ResponseSignals
from helpers import Logger
from models import ProjectModel,DataChunkModel,AssetModel
from models.db_schemas import DataChunk,Asset
from models import AssetTypeEnums

logger=Logger().get_logger()


data_router=APIRouter(prefix="/data")

@data_router.post("/upload/{project_id}")
async def upload_file(request:Request, project_id:str,file: UploadFile= File(None),app_settings: Settings = Depends(get_settings)):
    

    project=await ProjectModel.create_instance(request.app.db_client)
    project=await project.get_project_or_create_one(project_id)
    
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

    assetModel=await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource=  Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnums.FILE.value,
        asset_name=file.filename,
        asset_size=os.path.getsize(file_path))

    asset_record=await assetModel.create_asset(asset=asset_resource)


    return JSONResponse(
            content={"message": ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value 
                    ,"project_id":str(asset_record.id)
                    
                     }
        )



@data_router.post("/process/{project_id}")
async def process_file(request:Request,project_id:str,process_request:ProcessRequest):
    

    
    

    project=await ProjectModel.create_instance(request.app.db_client)
    project=await project.get_project_or_create_one(project_id)
    
    
    chunk_size=process_request.chunck_size
    overlap_size=process_request.overlap_size



    
    
    
    processController=ProcessController(project_id=project_id)

    project_file_ids={}

    assetModel=await AssetModel.create_instance(db_client=request.app.db_client)
    if process_request.file_id:
        asset_record=await assetModel.get_asset_record(
            asset_name=process_request.file_id,
            asset_project_id=project.id

        )
        if asset_record:
            project_file_ids={asset_record.id:asset_record.asset_name}
        else:
            return JSONResponse(
            status_code=400,
            content={

                "signal":ResponseSignals.NO_FILES_ERROR.value
            }
            )
    else:
        
        project_files=await assetModel.get_all_project_asset(asset_project_id=project.id,asset_type=AssetTypeEnums.FILE.value)
        
        logger.debug(f"project_files count is {len(project_files)} {project_files} project_id {str(project.id)} ")
        project_file_ids={
                record.id:record.asset_name
                for record in project_files
        }
        
    if len(project_file_ids)==0:
        return JSONResponse(
            status_code=400,
            content={

                "signal":ResponseSignals.NO_FILES_ERROR.value
            }

        )
    number_of_chunks=0
    number_of_files=0
    logger.debug(f"project_file_ids {project_file_ids}")
    for asset_id,file_id in project_file_ids.items():

        logger.debug(f"file id {file_id}")

        file_content= processController.get_file_content(file_id)

        file_chunks=processController.process_file_content(file_content,file_id,chunk_size,overlap_size)

        if file_chunks is None or len(file_chunks)==0: 
            return JSONResponse(
                status_code=400,
                content={
                    "signal": ResponseSignals.FILE_PROCESSED_FAILED.value
                }

            )
        logger.debug(f" chunks {file_chunks} {file_chunks[0].page_content}")

        file_chunks_records=[


            DataChunk(chunk_text=chunk.page_content,chunk_metadata=chunk.metadata,chunk_order=i+1,chunk_project_id=project.id
                      ,chunk_asset_id=asset_id)
            for i,chunk in enumerate(file_chunks)
        ]


        chunkModel=await DataChunkModel.create_instance(db_client=request.app.db_client)
        number_of_files+=1
        number_of_chunks+=await chunkModel.insert_many_chunks(chunks=file_chunks_records)
    return  JSONResponse(
        
        content={

            "number_of_files":number_of_files,
            "number_of_chunks":number_of_chunks
        }

    )