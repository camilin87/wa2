# Return Code classes
# 0 - 99 Reserved

# 100 - 199 Warnings
#           Warnings are still successful responses.
#           However, they need to be taken care of
OBSOLETE_API = 100

# 200 - 299 Success
OK = 200

# 300 - 399 Client api key error
PARAM_KEY_ERROR = 300
PARAM_LAT_ERROR = 301
PARAM_LONG_ERROR = 302
ERROR_BUILDING_REQUEST = 304

# 400 - 499 Designed Api Errors
API_SHUTDOWN = 400

# 500 - 599 Unexpected Errors
UNEXPECTED_ERROR = 500
EXTERNAL_API_ERROR = 550
