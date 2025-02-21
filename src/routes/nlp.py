from fastapi import FastAPI, APIRouter, status, Request

from fastapi.responses import JSONResponse
from helpers import Logger
from routes.schemas.PushRequest import PushRequest
from routes.schemas.SearchRequest import SearchRequest
from models import ProjectModel
from controllers import NLPController
from models import ResponseSignals,DataChunkModel
from models.db_schemas import DataChunk





nlp_router=APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"]
                     )


@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request,project_id:str,push_request:PushRequest):
    logger=Logger().get_logger()
    project=await ProjectModel.create_instance(request.app.db_client)
    project=await project.get_project_or_create_one(project_id)

    nlpController=NLPController(request.app.vector_db_client,request.app.generation_client,request.app.embedding_client)

    if not project : 
        return JSONResponse(
            status_code=400,
            content={
                "message":ResponseSignals.PROJECT_NOT_FOUND.value
            }
            
        )


    dataChunkModel=await DataChunkModel.create_instance(request.app.db_client)

    page_no=1
    chunks_count=0
    idx=0
    logger.debug("starting the while")
    while True:
        
        chunks_list=await dataChunkModel.get_project_chunks(project_id=project.id,page_no=page_no,page_size=100)
        logger.debug(f"in the while {len(chunks_list)} project_id is {project_id}")
        if not chunks_list or len(chunks_list)==0:
            break
        
        chunks_ids=list(range(idx,idx+len(chunks_list)))
        idx+=len(chunks_list)
        page_no+=1

        chunks_count+=len(chunks_list)
        is_inserted=nlpController.index_into_vector_db(project=project,chunks=chunks_list,chunks_ids=chunks_ids,do_reset=push_request.do_reset)
        
        if not is_inserted:
            return JSONResponse(
                status_code=400,
                content={
                    "message":ResponseSignals.INSERTION_PROBLEM.value
                }
                
             )


    return JSONResponse(
                content={
                    "message":ResponseSignals.INSERTION_SUCCESSFULLY.value,
                    "count":chunks_count
                }
                
             )

    


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request:Request, project_id:str):
    project_model=await ProjectModel.create_instance(request.app.db_client)
    project=await project_model.get_project_or_create_one(project_id)


    nlp_controller=NLPController(vector_db_client=request.app.vector_db_client,
                                 embedding_client=request.app.embedding_client,
                                 generation_client=request.app.generation_client
                                 )
    
    collection_info= nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(

        content={
            "signal": "some signal should be correct",
            "collection_info":collection_info
        }

    ) 



@nlp_router.post("/index/search/{project_id}")
async def search_indext(request:Request,project_id:str,search_request:SearchRequest):

    project=await ProjectModel.create_instance(request.app.db_client)
    project=await project.get_project_or_create_one(project_id)

    nlp_controller=NLPController(
                                vector_db_client=request.app.vector_db_client,
                                 embedding_client=request.app.embedding_client,
                                 generation_client=request.app.generation_client)
    
    results=nlp_controller.search_vector_db_collection(project=project,text=search_request.text,limit=search_request.limit)


    if not results:
         

         return JSONResponse(

            content={
                "signal": "so baad",
            }   

        ) 
    


    return JSONResponse(

        content={
            "signal": "searching index done successfully",
            "results":results
        }

    ) 




    
