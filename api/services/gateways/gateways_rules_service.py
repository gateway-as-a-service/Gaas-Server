import time

from bson import ObjectId

import api.server
from api.libs.utils import MongoUtils


class RulesService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.rules_collection = MongoUtils.rules

    def create(self, rule):
        if rule.get("_id"):
            rule["_id"] = ObjectId(rule["_id"])

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

    def update_rule(self, rule_id, gateway_uuid, ):
        pass


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
    #     '8730862f-84da-4916-9c82-4889aa768aec', '0dea48da-3f48-4ba4-ab88-9d0f1de41bec',
    #     '9e75730e-c0a8-433d-b8f1-004e8908414a', 'cc367153-3ba2-4e86-b673-002210612094',
    #     '4c77b947-e8d0-49bc-9a92-e0cfa5c45346', 'a4c2c5fc-939e-408f-b1c3-238aa280a4e0',
    #     '3acc2551-e70d-467c-b755-e6b7820dbbfb', 'b99db5ed-9a8a-4684-b21b-18ea21c8baab',
    #     '53486061-90dc-4bac-9afd-7460bac9463f', '83a3f6f8-23bd-4df0-b307-795abbdce7f7'
    # ]

    DEVICES_UUIDS = [
        '017c257b-01da-48e5-b8e4-e3b2d2f1797b', 'b5c406c8-9d1e-491e-aaeb-a6971dd05135',
        'c04bdd1e-8e8f-4852-8088-cfa97196031d', 'edd4e981-7155-41ad-8a0f-da4ff8f25033',
        'adb6c602-43fb-41b4-8c9a-834fd1fcf646', 'ba80f391-df1d-4164-9686-240fa8733ec2',
        '8a52d240-ebcc-4a5a-82aa-c16879ac136c', '4d364d23-3d3c-4e9a-ab68-67dbe9cebf9b',
        'b07a0931-5a2b-4a9e-83a9-546c6f55fab3', '1ebed9e6-c948-4bc3-8065-e86aff2f7df4',
        'b2b9cd9e-1b6b-422a-9475-760684ef8caa', '178a4756-bc30-4266-ba4c-cf861fec14c6',
        '1eaa0a19-48e8-447d-a10d-76af3fe44532', '22eecd76-dfbe-49a5-970a-75d7b88a513c',
        '8ae3d31b-e095-46b5-808d-3b9f88fd2f0e', '1a642569-409c-4f02-b54b-8cc3f43ffbc4',
        'fa5f86ad-3f8a-4202-9eab-f1cbc2766c3b', '55608f1e-5d26-43e6-8d71-f8bf9d3dbb5e',
        '8bb75926-65f2-4d13-a187-333384507958', '0bfa5246-4346-405f-bcb2-ad30cb4d4211'
    ]
    _create_performance_test_rules(DEVICES_UUIDS)
