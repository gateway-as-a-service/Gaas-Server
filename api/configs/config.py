import os

from dotenv import load_dotenv

load_dotenv()


class ACTIONS_TYPES(object):
    RULE_TRIGGERED = "RULE_TRIGGERED"
    CHANGE_VALUE = "CHANGE_VALUE"


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 6000
SERVER_NAME = "GaaS Server"
SERVER_API_VERSION = "v1"

MONGO_DB_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_URI = "mongodb+srv://{}:{}@gaasservercluster-drlqv.mongodb.net/GaaS_Server?retryWrites=true" \
    .format(MONGO_DB_USERNAME, MONGO_DB_PASSWORD)
MONGO_DB_NAME = "GaaS_Server"
