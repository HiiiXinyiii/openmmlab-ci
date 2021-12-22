from enum import Enum


INVALID_FORMAT_PAIRS = [
    ["aaa", "bbb"],
    ["", "JgPZ1ezGocppg4JO51zmXLwq"],
    [None, "JgPZ1ezGocppg4JO51zmXLwq"],
    ["JgPZ1ezGocppg4JO51zmXLwq", ""],
    ["JgPZ1ezGocppg4JO51zmXLwq", "中文"],
    [None, None]
]


OPENAPI_SERVER  = "https://platform.openmmlab.com"
USER_SERVICE    = "/gw/user-service"
UPLOAD_SERVICE  = "/gw/upload-service"
INF_SERVICE     = "/gw/model-inference"
# create user
# create auth
AUTH_URI         = "/api/v1/openapi/auth"
AUTH_CREATE_URI  = "/api/v1/openapi/accessKey/create"
# inf service
API_URI          = "/openapi/v1/"
ASYNC_RESULT     = "/openapi/v1/getResult"
# upload file
UPLOAD_URI       = "/api/v1/uploadFile"


class CODEB(Enum):
    CLS          = "classification"
    DET          = "detection"
    SEG          = "segmentation"
    SUP          = "superResolution"
    POSE         = "pose"
    ACTION       = "action"


class FILE_TYPE(Enum):
    ID           = "ID"
    URL          = "URL"

# default value
DEFAULT_CLS_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "Swin-Transformer",
    "dataset": "ImageNet"
}
DEFAULT_DET_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "YOLOX"
}
DEFAULT_SEG_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "YOLOX"
}
DEFAULT_SUP_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "YOLOX"
}
DEFAULT_POSE_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "YOLOX"
}
DEFAULT_ACTION_BODY  = {
    "backend": "PyTorch",
    "resource": "https://platform.openmmlab.com/web-demo/static/one.b7608e9b.jpg",
    "resourceType": "URL",
    "requestType": "SYNC",
    "algorithm": "YOLOX"
}
DEFAULT_CODEB     = CODEB.CLS
DEFAULT_FILE_ID   = "one.e9be6cd7.jpg"
DEFAULT_FILE_TYPE = FILE_TYPE.ID.value
DEFAULT_FILE_URL  = "https://oss.openmmlab.com/openmmlab-demo/tmp_e2b4d57f.jpeg"
DEFAULT_TOKEN     = "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJyb2wiOiJST0xFX1JFR0lTVEVSX1VTRVIiLCJqdGkiOiIxMzk1OTciLCJpc3MiOiJTbmFpbENsaW1iIiwiaWF0IjoxNjM5OTc4NTQ2LCJzdWIiOiJkZWwtemhlbnd1MSIsImV4cCI6MTY0MDU4MzM0Nn0.Ow9m8uWIQmFRSoQQl0z9rRro5IsXwjvdk1TbwQgltllo2-FpeclPBdhbc60wNUq-T9b0S-Wt_seRjFmQ9skjKA"