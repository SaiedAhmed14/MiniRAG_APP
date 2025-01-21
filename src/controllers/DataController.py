from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignals
class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale=1048576

    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False ,ResponseSignals.FILE_TYPE_NOT_SUPPORTED

        if file.size>self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False ,ResponseSignals.FILE_SIZE_EXCEEDED
        
        return True ,ResponseSignals.File_validate_success
    
    
    