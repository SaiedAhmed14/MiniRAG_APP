from enum import Enum
class ResponseSignals(Enum):
    FILE_TYPE_NOT_SUPPORTED="file_type_not_supported"
    FILE_SIZE_EXCEEDED="file_size_exceeded"
    FILE_UPLOADED_SUCCESS="file_uploaded_success"
    FILE_UPLOADED_FAILED="file_uploaded_failed"
    File_validate_success="file_validate_success"
    File_validate_failed="file_validate_failed"
    PROCESSING_SUCCESS="processing_success"
    PROCESSING_FAILED="processing_failed"