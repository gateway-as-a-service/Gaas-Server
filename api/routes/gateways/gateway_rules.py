from flask import jsonify
from flask import request
from flask.views import MethodView

import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_rules_service import RulesService


class GatewayRulesView(MethodView):

    def __init__(self):
        self.gateway_rules_service = RulesService()

    def get(self, gateway_uuid):
        gateway_uuid = str(gateway_uuid)
        rules = self.gateway_rules_service.find_from_gateway(gateway_uuid)
        for rule in rules:
            rule["_id"] = str(rule["_id"])

        return jsonify(rules), HTTPStatusCodes.OK
