import api.server
from api.libs.exceptions import FailedRequestException
from api.libs.utils import MongoUtils


class RulesHistoryService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.rules_history_collection = MongoUtils.rules_history

    def create(self, rule_history):
        try:
            return self \
                .rules_history_collection \
                .insert_one(rule_history) \
                .inserted_id

        except Exception as err:
            self.logger.error("Failed to insert the rule history. Reason: {}".format(err), exc_info=True)
            return None

    def insert_multiple(self, rules_history):
        try:
            return self \
                .rules_history_collection \
                .insert_many(rules_history)

        except Exception as err:
            self.logger.error(
                "Failed to append the new history rules. Reason: {}".format(err), exc_info=True,
            )
            raise FailedRequestException("Failed to add the rule trigger history")

    def find_history(self, rule_id):
        try:
            return self \
                .rules_history_collection \
                .find({"rule_id": rule_id}) \
                .sort({"timestamp": -1})

        except Exception as err:
            self.logger.error(
                "Failed to retrieve history of rule: {}. Reason: {}".format(rule_id, err), exc_info=True
            )
            raise FailedRequestException("Failed to retrieve the rule's history")
