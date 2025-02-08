from enum import Enum

class ResponseSignals(Enum):

    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_SIZE_EXCEEDED= "file size exceeded"
    FILE_UPLOADED_SUCCESSFULLY=" file uploaded successfully"
    FILE_UPLOADED_FAILED= "filed uploaded failed"
