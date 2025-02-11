from .BaseDataModel import BaseDataModel
from . import DatabaseEnums
from db_schemas import DataChunk

class DataChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection=self.db_client[DatabaseEnums.CHUNK_COLLECTION_NAME.value]

    async def create_data_chunk(self,chunk:DataChunk):
        result=self.collection.insert_one(chunk.dict())
        


