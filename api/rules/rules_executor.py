import api.server
from api.configs.config import ACTIONS_TYPES
from api.libs.utils import get_utc_timestamp
from api.services.gateways.gateways_devices_service import DevicesService
from api.services.gateways.gateways_rules_service import RulesService
from api.rules.rules_engine import RulesEngine


class RulesExecutor(object):

    def __init__(self):
        self.logger = api.server.app.logger

        self.rules_service = RulesService()
        self.rules_engine = RulesEngine()
        self.devices_service = DevicesService()

    def execute(self, rules):
        if not rules:
            return []

        performed_actions = []
        rules_to_check = list(rules)
        while rules_to_check:
            new_rules_to_check = []
            for rule in rules_to_check:
                rule_id = str(rule["_id"])
                self.logger.debug("Process rule {}".format(rule_id))

                devices = self.devices_service.find_multiple_devices(rule["devices_involved"])
                device_id_to_value = {device["id"]: device["value"] for device in devices}
                missing_devices = set(rule["devices_involved"]) - device_id_to_value.keys()
                if missing_devices:
                    self.logger.error("Some devices are missing {}".format(missing_devices))
                    continue

                rule_was_triggered = self.rules_engine.evaluate_rule(rule, device_id_to_value)
                if not rule_was_triggered:
                    self.logger.debug("Rule {} has been evaluated and wasn't triggered".format(rule_id))
                    continue

                performed_actions.append(
                    {"type": ACTIONS_TYPES.RULE_TRIGGERED, "rule": rule_id, "timestamp": get_utc_timestamp()}
                )
                self.logger.debug(
                    "Rule {} has been evaluated and it was triggered. Perform the in cause actions"
                        .format(rule_id)
                )
                actions_to_do = rule["actions"]
                if not actions_to_do:
                    self.logger.debug("No actions has to be performed for rule {}".format(rule_id))
                    continue

                self.devices_service.update_multiple(actions_to_do)
                updated_devices_ids = []
                for device_id, new_value in actions_to_do.items():
                    performed_actions.append(
                        {
                            "type": ACTIONS_TYPES.CHANGE_VALUE, "device": device_id, "value": new_value,
                            "timestamp": get_utc_timestamp()
                        }
                    )
                    updated_devices_ids.append(device_id)

                new_rules = list(self.rules_service.find_than_involves_devices(updated_devices_ids))
                self.logger.debug("Have to check {} other rules".format(len(new_rules)))
                new_rules_to_check.extend(new_rules)

            rules_to_check = new_rules_to_check

        return performed_actions
