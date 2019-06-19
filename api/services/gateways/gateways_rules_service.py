import time

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

    def find_from_gateway(self, gateway_uuid):
        criteria = {'gateway_uuid': gateway_uuid}

        try:
            rules = self.rules_collection.find(criteria) or []
            return list(rules)
        except Exception as err:
            self.logger.error(
                "Failed to retrieve the rules from gateway {}. Reason: {}"
                    .format(gateway_uuid, err), exc_info=True
            )

    def update_last_trigger(self):
        try:
            self.rules_collection.update_many({}, {'$set': {'last_trigger': time.time()}})
        except Exception as err:
            self.logger.error(
                "Failed to update the trigger time for all rules. Reason: {}".format(err), exc_info=True
            )

    def update_rule_last_trigger(self, _id, last_trigger):
        try:
            return self.rules_collection \
                       .update_one({'_id': ObjectId(_id)}, {'last_trigger': last_trigger}) \
                       .matched_count > 0
        except Exception as err:
            self.logger.error(
                "Failed to update the last trigger for rule {}. Reason: {}".format(_id, err), exc_info=True
            )


def _create_performance_test_rules(ids: list):
    rules_service = RulesService()
    for id in ids:
        rule = {
            "postfix": [
                "A",
            ],
            "name": "Simple Rule",
            "conditions": {
                "A": {
                    "device_id": id,
                    "operator": ">",
                    "value": 20
                },
            },
            "devices_involved": [
                id,
            ],
            "actions": {},
        }
        rule["actions"][id] = 18

        rules_service.create(rule)


if __name__ == '__main__':
    rules_service = RulesService()
    rules_service.update_last_trigger()

    # DEVICES_UUIDS = [
    #     'd788f2b1-6080-4570-ae55-ed71eb146a1a', '0273cbca-7a4a-4dca-87db-1268761337e4',
    #     '6201d03d-640f-4a2e-aed9-9d6dc037f73b', 'b8758601-4726-48ff-9457-87b6240c70ac',
    #     '7115f32b-c84b-4dbc-9e53-b56476d68fc7', '7e2f23a3-fbea-4843-bc79-0f04b9596abe',
    #     'ff82767e-6bab-4af7-bfe3-534100f3b2eb', 'a9cc8991-a99a-420f-8865-a29d745631fe',
    #     'f8bcf0f9-fadb-46fe-a251-472e559e91df', '286d0581-3296-4923-ba90-7bd343bf17e0',
    #     '8730862f-84da-4916-9c82-4889aa768aec', '0dea48da-3f48-4ba4-ab88-9d0f1de41bec',
    #     '9e75730e-c0a8-433d-b8f1-004e8908414a', 'cc367153-3ba2-4e86-b673-002210612094',
    #     '4c77b947-e8d0-49bc-9a92-e0cfa5c45346', 'a4c2c5fc-939e-408f-b1c3-238aa280a4e0',
    #     '3acc2551-e70d-467c-b755-e6b7820dbbfb', 'b99db5ed-9a8a-4684-b21b-18ea21c8baab',
    #     '53486061-90dc-4bac-9afd-7460bac9463f', '83a3f6f8-23bd-4df0-b307-795abbdce7f7'
    # ]
    # _create_performance_test_rules(DEVICES_UUIDS)
