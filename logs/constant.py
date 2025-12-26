from datetime import datetime
class Constant:
    LOGS_SRATE_DATA = datetime(year=2024, month=1, day=1,hour=0,minute=0,second=0)
    LOGS_END_DATA = datetime(year=2025, month=1, day=1,hour=0,minute=0,second=0)
    NUMBER_OF_LOGS = 100000
    HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
    API_ENDPOINTS = ["/users","/admin","/login","/data","/metrics"]
    HTTP_NORMAL_CODES : list[str] = [200, 201, 204]
    HTTP_ERROR_CODES: dict[str, list[str]] = {
        "client_errors": [400, 401, 403, 404],
        "server_errors": [500, 502, 503],
        "timeout_errors": ["408","504"]

    }
    NUMBER_OF_ANOMALIES_INTRVALS :int = 5
    MIN_NUMBER_OF_ANOMALIES_PER_INTRVALS :int = 500
    MAX_NUMBER_OF_ANOMALIES_PER_INTRVALS :int = 1000
    NUMBER_OF_ANOMALIES_IPS :int = 15
    LOGS_DATA_FILE_NAME = "data/logs_dataset.csv"
