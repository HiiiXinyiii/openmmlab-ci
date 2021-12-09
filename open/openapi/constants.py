

INVALID_FORMAT_PAIRS = [
    ("aaa", "bbb"),
    ("", "JgPZ1ezGocppg4JO51zmXLwq"),
    (None, "JgPZ1ezGocppg4JO51zmXLwq"),
    ("JgPZ1ezGocppg4JO51zmXLwq", ""),
    ("JgPZ1ezGocppg4JO51zmXLwq", "中文"),
    (None, None)
]


OPENAPI_SERVER  = "https://open.openmmlab.com"
USER_SERVICE    = "/gw/user-service"

# create user
# create auth
AUTH_URI        = "/api/v1/openapi/auth"
AUTH_CREATE_URI = "/api/v1/openapi/accessKey/create"
