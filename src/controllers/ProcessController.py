from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter
################################################
class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)
  
    #TODO: get file extension################################################
    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    #TODO: get file loader################################################
    def get_file_loader(self,file_id:str):
        file_ext=self.get_file_extension(file_id=file_id)
        file_path=os.path.join(self.project_path,file_id)
        if file_ext.lower()==ProcessingEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")
        elif file_ext.lower()==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None
    #TODO: get file content ################################################
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()
    #TODO: process file content################################################
    def process_file_content(self,file_content:list,file_id:str,chunk_size: int=100, overlap_size: int=20):
        
        #determine chunk properties################################################ 
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=10,
            length_function=len,
        )
        #extract text content################################################
        file_content_text=[
            rec.page_content
            for rec in file_content
        ]
        #extract metadata content################################################
        file_content_metadata=[
            rec.metadata
            for rec in file_content
        ]
        #Craete chunks################################################
        chunks=text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
        )
        return chunks
    

