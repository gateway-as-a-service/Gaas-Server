import datetime
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from pymongo import MongoClient

from api.configs.config import MONGO_DB_NAME, MONGO_DB_URI
from api.configs.utils import LOGS_FOLDER


class MongoUtils(object):
    client = MongoClient(MONGO_DB_URI)
    database = client[MONGO_DB_NAME]

    gateways = database["gateways"]
    devices = database["devices"]
    devices_history = database["devices_history"]
    rules = database["rules"]
    rules_history = database["rules_history"]
    users = database["users"]


class FakeLogger(object):
    def __init__(self):
        pass

    def debug(self, message, **kwargs):
        print("[Fake Logger][DEBUG] {}".format(message))

    def info(self, message, **kwargs):
        print("[Fake Logger][INFO] {}".format(message))

    def warning(self, message, **kwargs):
        print("[Fake Logger][WARNING] {}".format(message))

    def error(self, message, **kwargs):
        print("[Fake Logger][ERROR] {}".format(message))

    def critical(self, message, **kwargs):
        print("[Fake Logger][CRITICAL] {}".format(message))


def register_logger(app):
    api_logs_folder = os.path.join(LOGS_FOLDER, "api")
    if not os.path.exists(api_logs_folder):
        os.mkdir(api_logs_folder)

    logger = app.logger
    log_file_path = os.path.join(api_logs_folder, "api.log")

    stream_handler = logging.StreamHandler(sys.stdout)
    rotating_file_handler = TimedRotatingFileHandler(log_file_path)
    formatter = logging.Formatter(
        "[%(asctime)-15s] - [%(levelname)s - %(filename)s - %(threadName)s] %(message)s")

    for handler in [stream_handler, rotating_file_handler]:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)


def get_utc_timestamp():
    return datetime.datetime.utcnow().timestamp()
