from .import BaseController
from models.db_schemas import Project,DataChunk
from typing import List
from stores import LLMEnums
from helpers import Logger
import json
class NLPController(BaseController):

    def __init__(self,vector_db_client,generation_client,embedding_client):
        super().__init__()

        self.vector_db_client=vector_db_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client
        
        self.logger=Logger().get_logger()

    def create_collection_name(self, project_id: str ):
        return f"collection_{project_id}".strip()


    def reset_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        self.vector_db_client.delete_collection(collection_name=collection_name)
    

    def get_vector_db_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        collection_info=self.vector_db_client.get_collection_info(collection_name=collection_name)
        
        return json.loads(

            json.dumps(collection_info,default=lambda x: x.__dict__)
        )
        


    def index_into_vector_db(self,project:Project, chunks:List[DataChunk],chunks_ids:List[int],do_reset: bool =True):

        collection_name=self.create_collection_name(project_id=project.project_id)

        texts=[c.chunk_text for c in chunks]

        meta_data=[c.chunk_metadata for  c in chunks]


        vectors=[

            self.embedding_client.embed_text(text,LLMEnums.DOCUMENT)

            for text in texts
        ]

        self.vector_db_client.create_collection(

            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset

        )
        

        self.logger.debug(f"we are inserting many {vectors[0]}")
        self.vector_db_client.insert_many(

            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=meta_data,
            record_ids=chunks_ids

        )



        return True
        
    def search_vector_db_collection(self,project:Project,text: str ,limit:int =10):

        collection_name=self.create_collection_name(project_id=project.project_id)

        vector=self.embedding_client.embed_text(

            text=text,
            document_type=LLMEnums.QEURY.value
        )

        
        if not vector or len(vector)==0:
            return False
        

        self.logger.debug(f" we are going to search by vector the collection_name is {collection_name}")
        results=self.vector_db_client.search_by_vector(

            vector=vector,
            limit=limit,
            collection_name=collection_name
        )

        
        self.logger.debug(f" the results after searching by vector {results}")
        if not results:
            return False
        

        return json.loads(

            json.dumps(results , default=lambda x:x.__dict__)
        )




