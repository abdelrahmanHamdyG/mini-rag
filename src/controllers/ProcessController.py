from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from helpers import Logger
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger=Logger().get_logger()



class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)


    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self,file_id:str):

        file_path=os.path.join(self.project_path,file_id)
        logger.debug(f"file path {file_path}")
        file_extension=self.get_file_extension(file_id)
        logger.debug(f"file extension {file_extension}")

        if file_extension ==".txt":
            return TextLoader(file_path,encoding="utf-8")
        elif file_extension==".pdf":
            return PyMuPDFLoader(file_path)
        return None
    

    def get_file_content(self,file_id):
        loader=self.get_file_loader(file_id)
        return loader.load()
    

    def process_file_content(self, file_content: list, file_id:str,chunk_size:int=100, over_lap:int =20):

        
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=over_lap,length_function=len)

        file_content_text=[rec.page_content for rec in file_content]

        file_content_meta_data=[rec.metadata for rec in file_content]

        chuncks = text_splitter.create_documents(file_content_text,metadatas=file_content_meta_data)

        return chuncks
    







    


