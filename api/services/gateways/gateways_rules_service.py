from bson import ObjectId

import api.server
from api.libs.utils import MongoUtils


class RulesService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.rules_collection = MongoUtils.rules

    def create(self, rule):
        try:
            return self.rules_collection.insert_one(rule).inserted_id

        except Exception as err:
            self.logger.error("Failed to insert the rule. Reason: {}".format(err))
            return None

    def find(self, _id):
        try:
            return self.rules_collection.find_one({"_id": ObjectId(_id)})
        except Exception as err:
            self.logger.error("Failed to retrieve the rule with _id {}. Reason:{}".format(_id, err))
            return None

    def find_than_involves_devices(self, devices_ids):
        try:
            return self.rules_collection.find({"devices_involved": {"$in": devices_ids}})
        except Exception as err:
            self.logger.error(
                "Failed to retrieve the rules that involves device {}. Reason: {}".format(devices_ids, err))
            return None
