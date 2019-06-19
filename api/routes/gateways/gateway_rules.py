from flask import jsonify
from flask import request
from flask.views import MethodView
import requests

import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_rules_service import RulesService
from api.services.gateways.gateways_service import GatewaysService


class GatewayRulesView(MethodView):

    def __init__(self):
        self.gateway_service = GatewaysService()
        self.gateway_rules_service = RulesService()

    def _send_rule_to_gateway(self, gateway_url, rule):
        url = "{}/api/rules".format(gateway_url)
        response = requests.post(url, json=rule)
        if not response:
            raise Exception("Failed to communicate with the gateway")

        return response.json()['_id']

    def post(self, gateway_uuid):
        rule = request.get_json()
        gateway = self.gateway_service.find(uuid=str(gateway_uuid))
        if not gateway:
            api.server.app.logger.error("Gateway {} don't exist".format(gateway_uuid))
            response = {
                "message": "Gateway not found"
            }
            return jsonify(response), HTTPStatusCodes.NOT_FOUND

        rule_id = self._send_rule_to_gateway(gateway["ip"], rule)
        rule["_id"] = rule_id
        self.gateway_rules_service.create(rule)

        return jsonify({'rule_id': rule_id}), HTTPStatusCodes.CREATED

    def get(self, gateway_uuid):
        gateway_uuid = str(gateway_uuid)
        rules = self.gateway_rules_service.find_from_gateway(gateway_uuid)
        for rule in rules:
            rule["_id"] = str(rule["_id"])

        return jsonify(rules), HTTPStatusCodes.OK

    def put(self, gateway_uuid, rule_id):
        body = request.get_json()
        body.pop("_id", None)
        print(gateway_uuid, rule_id, body)

        return jsonify({}), HTTPStatusCodes.NO_CONTENT
