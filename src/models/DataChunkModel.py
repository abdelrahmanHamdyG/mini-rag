from .BaseDataModel import BaseDataModel
from . import DatabaseEnums
from .db_schemas import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class DataChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection=self.db_client[DatabaseEnums.CHUNK_COLLECTION_NAME.value]

    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance
        


    async def init_collection(self):
        all_collection=await self.db_client.list_collection_names()
        if DatabaseEnums.CHUNK_COLLECTION_NAME.value not in all_collection:
            self.collection=self.db_client[DatabaseEnums.CHUNK_COLLECTION_NAME.value]
            indexes=DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"],name=index["name"],unique=index["unique"])

    
    async def create_data_chunk(self,chunk:DataChunk):
        result=self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id=result.inserted_id
        return chunk 
    
    async def get_chunk(self,chunk_id):

        result=await self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })

        if result is None:
            return None

        return DataChunk(**result)
    

    async def insert_many_chunks(self,chunks: list, batch_size: int =100):
        for i in range(0,len(chunks),batch_size):
            current_batch=chunks[i:i+batch_size]

            operations=[InsertOne(chunk.dict(by_alias=True,exclude_unset=True)) for chunk in current_batch ]
            await self.collection.bulk_write(operations)

        return len(chunks)

        


