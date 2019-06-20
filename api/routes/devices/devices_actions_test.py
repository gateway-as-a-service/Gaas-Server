from flask import jsonify
from flask import request
from flask.views import MethodView
import api.server
from api.configs.utils import HTTPStatusCodes
from api.rules.rules_executor import RulesExecutor
from api.services.fcm_service import FcmService
from api.services.gateways.gateways_devices_history_service import DevicesHistoryService
from api.services.gateways.gateways_devices_service import DevicesService
from api.services.gateways.gateways_rules_history import RulesHistoryService
from api.services.gateways.gateways_rules_service import RulesService
from api.services.users.users_service import UserService


class GatewayDevicesActionsViewTest(MethodView):

    def __init__(self):
        self.devices_service = DevicesService()
        self.devices_history_service = DevicesHistoryService()
        self.rules_service = RulesService()
        self.rules_history_service = RulesHistoryService()
        self.user_service = UserService()

        self.rules_executor = RulesExecutor()

        self.fcm_service = FcmService()

    def _parse_device_new_value_action(self, action, gateway_uuid):
        rules = self.rules_service.find_than_involves_devices([action['device']])
        self.rules_executor.execute(rules)

    def post(self, gateway_uuid):
        gateway_uuid = str(gateway_uuid)
        body = request.get_json()
        api.server.app.logger.info("Devices actions Body: {}".format(body))

        for action in body:
            self._parse_device_new_value_action(action, gateway_uuid)

        response = {
            "message": "Actions has been registered",
        }
        return jsonify(response), HTTPStatusCodes.CREATED
