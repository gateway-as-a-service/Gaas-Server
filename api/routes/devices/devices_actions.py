import api.server

from flask.views import MethodView
from flask import request
from flask import jsonify

from api.configs.config import ACTIONS_TYPES
from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_devices_service import DevicesService
from api.services.gateways.gateways_devices_history_service import DevicesHistoryService
from api.services.gateways.gateways_rules_service import RulesService
from api.services.gateways.gateways_rules_history import RulesHistoryService


class GatewaysDevicesActionsView(MethodView):
    POST_REQUIRED_FIELDS = {
        ACTIONS_TYPES.RULE_TRIGGERED: {"type", "rule", "timestamp", },
        ACTIONS_TYPES.CHANGE_VALUE: {"type", "device", "value", "timestamp"},
    }

    def __init__(self):
        self.devices_service = DevicesService()
        self.devices_history_service = DevicesHistoryService()
        self.rules_service = RulesService()
        self.rules_history_service = RulesHistoryService()

    def _validate_post_body(self, body):
        for action in body:
            if not isinstance(action, dict):
                return "All actions must be provided as an object"

            if not action.get("type"):
                return "All the actions must have their type"

            if action["type"] not in self.POST_REQUIRED_FIELDS:
                api.server.app.logger.debug("Received unknown type of action: {}".format(action["type"]))
                continue

            missing_fields = self.POST_REQUIRED_FIELDS[action["type"]] - action.keys()
            if missing_fields:
                return "Missing fields: {}".format(missing_fields)

    def _update_devices_values(self, actions, gateway_uuid):
        if not actions:
            return

        devices_new_history = []
        devices_new_values = {}
        for action in actions:
            devices_new_history.append({
                "device_uuid": action["device"],
                "value": action["value"],
                "timestamp": action["timestamp"],
                "gateway_uuid": gateway_uuid,
            })
            devices_new_values[action["device"]] = action["value"]

        self.devices_history_service.insert_multiple(devices_new_history)
        for device_id, new_device_value in devices_new_values.items():
            self.devices_service.update_device_value(device_id, new_device_value)

    def _update_rule_triggered(self, actions, gateway_uuid):
        if not actions:
            return

        rules_history = []
        for action in actions:
            rules_history.append({
                "rule_id": action["rule"],
                "timestamp": action["timestamp"],
                "gateway_uuid": gateway_uuid,
            })

        self.rules_history_service.insert_multiple(rules_history)

    def post(self, gateway_uuid):
        body = request.get_json()
        validation_error_message = self._validate_post_body(body)
        if validation_error_message:
            api.server.app.logger.warning(
                "Some error occurred during the validation of the body. Reason: {}"
                    .format(validation_error_message)
            )
            response = {
                "message": validation_error_message,
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        api.server.app.logger.info("Devices actions Body: {}".format(body))
        performed_actions = {
            ACTIONS_TYPES.CHANGE_VALUE: [],
            ACTIONS_TYPES.RULE_TRIGGERED: [],
        }
        for action in body:
            if action["type"] == ACTIONS_TYPES.CHANGE_VALUE:
                performed_actions[ACTIONS_TYPES.CHANGE_VALUE].append(action)
            elif action["type"] == ACTIONS_TYPES.RULE_TRIGGERED:
                performed_actions[ACTIONS_TYPES.RULE_TRIGGERED].append(action)

        self._update_devices_values(performed_actions[ACTIONS_TYPES.CHANGE_VALUE], str(gateway_uuid))
        self._update_rule_triggered(performed_actions[ACTIONS_TYPES.RULE_TRIGGERED], str(gateway_uuid))

        response = {
            "message": "Actions has been registered"
        }
        return jsonify(response), HTTPStatusCodes.CREATED
