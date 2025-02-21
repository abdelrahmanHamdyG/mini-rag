from ..VectorDBInterface import VectorDBInterface
from qdrant_client import models,QdrantClient
from ..VectorDBEnums import VectorDBEnums
from helpers import Logger


class QdrantDB(VectorDBInterface):
    def __init__(self,db_path:str, distance_method:str):

        self.db_path=db_path
        self.distance_method=None
        self.client=None
        self.logger=Logger().get_logger()

        if distance_method==VectorDBEnums.DOT.value:
            self.distance_method=models.DISTANCE.DOT
        
        if distance_method==VectorDBEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
    



    def connect(self):
        self.client=QdrantClient(path=self.db_path)


    def disconnect(self):
        self.client=None   

    
    def is_collection_existed(self, collection_name:str):
        return self.client.collection_exists(collection_name=collection_name)
    

    def list_all_collections(self):
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name):
        return self.client.get_collection(collection_name=collection_name)
    

    def delete_collection(self, collection_name):

        if self.is_collection_existed(collection_name):
            self.client.delete_collection(collection_name=collection_name)

    def create_collection(self, collection_name, embedding_size, do_reset = False):
        

        if do_reset:
            self.delete_collection(collection_name)
        
        if not self.is_collection_existed(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(

                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True
        return False



    def insert_one(self, collection_name, text, vector, metadata = None, record_ids = None, batch_size = 50):
        if not self.is_collection_existed(collection_name):
            return False
        
        self.client.upload_records(

            collection_name=collection_name,    
            records=[
                models.Record(
                    id=[record_ids],
                    vector=vector,
                    payload={
                        "text":text,"metadata":metadata
                    }
                )
            ]
        )
        return True


    def insert_many(self, collection_name, texts:list, vectors, metadata = None, record_ids = None, batch_size = 50):
        
        number_of_texts=len(texts)
        if metadata is None:
            metadata=[None]*number_of_texts
        
        if record_ids is None:
            record_ids=list(range(0,len(texts)))

        for i in range(0,number_of_texts,batch_size):
            batch_end=i+batch_size

            batch_text=texts[i:batch_end]
            batch_record_ids=record_ids[i:batch_end]
            batch_metadata=metadata[i:batch_end]
            batch_vectors=vectors[i:batch_end]

            batch_records=[
               
                models.Record(
                id=batch_record_ids[j],
                vector=batch_vectors[j],
                payload={
                    "text":batch_text[j],
                    "metadata":batch_metadata[j]
                })
                for j in range(len(batch_text))
            ]

            try:
                _=self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records
                )
            except Exception as e:
                self.logger.debug(f"error is {e}")
                return False
        return True
    



    def search_by_vector(self, collection_name, vector, limit):

        self.logger.debug(f"we are inside Qdrant DB search by vector {collection_name} and vector {vector}  and limit {limit}" )

        result=self.is_collection_existed(collection_name)
        self.logger.debug(f" does collection exists {result}" )
        return self.client.search(

            collection_name=collection_name,
            query_vector=vector,
            limit=limit

        )
    
    



