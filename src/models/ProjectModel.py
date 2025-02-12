from .BaseDataModel import BaseDataModel
from . import DatabaseEnums
from .db_schemas import Project
class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection=self.db_client[DatabaseEnums.PROJECT_COLLECTION_NAME.value]


    async def create_project(self,project:Project):
        result=await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project.id=result.inserted_id
        return project
    

    async def get_project_or_create_one(self,project_id:str):

        record=await self.collection.find_one({

            "project_id":project_id

        })

        if record is None:
            project= Project(project_id=project_id)

            result=await self.create_project(project)

            return result
        return Project(**record)
    
    async def get_all_projects(self,page:int = 1, limit:int =20):

        total_documents=self.collection.count_documents({})

        total_pages=total_documents//limit

        if total_pages%limit !=0 : 
            total_pages+=1
        cursor=self.collection.find().skip((page-1)*limit).limit(limit)
        projects=[]
        async for project in cursor:
            projects.append(Project(**project))


        return projects,total_pages
    

        








