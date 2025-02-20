from fastapi import FastAPI

from routes import data,base,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBFactory import VectorDBFactory

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings=get_settings()
    app.mongo_conn=AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client=app.mongo_conn[settings.MONGO_DATABASE]

    llmProviderFactory=LLMProviderFactory(settings)

    vector_db_factory=VectorDBFactory(settings)

    app.generation_client=llmProviderFactory.create(provider=settings.GENERATION_BACKEND)
    
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    
    app.embedding_client=llmProviderFactory.create(provider=settings.EMBEDDING_BACKEND)    
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)
    app.vector_db_client=vector_db_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()





@app.on_event("shutdown")
async def shutdown_db_client():
    
    app.mongo_conn.close() 
    app.vector_db_client.disconnect()


app.on_event("startup")(startup_db_client)
app.on_event("shutdown")(shutdown_db_client)
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

