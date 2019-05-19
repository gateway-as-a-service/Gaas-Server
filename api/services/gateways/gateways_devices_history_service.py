import api.server
from api.libs.exceptions import FailedRequestException
from api.libs.utils import MongoUtils


class DevicesHistoryService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.devices_history = MongoUtils.devices_history

    def insert_multiple(self, history: list):
        try:
            return self \
                .devices_history \
                .insert_many(history)

        except Exception as err:
            self.logger.error("Failed to add append the new history. Reason: {}".format(err))
            raise FailedRequestException("Failed to append the history")
