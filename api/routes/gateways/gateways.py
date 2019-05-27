from flask import jsonify
from flask import request
from flask.views import MethodView

import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_service import GatewaysService


class GatewaysView(MethodView):
    POST_BODY_REQUIRED_FIELDS = {"uuid", "name", "description", "ip", "port"}

    def __init__(self):
        api.server.app.logger = api.server.app.logger

        self.gateways_service = GatewaysService()

    def _validate_post_body(self, body):
        if not isinstance(body, dict):
            return "Body must be an object"

        missing_keys = self.POST_BODY_REQUIRED_FIELDS - body.keys()
        if missing_keys:
            return "Missing keys: {}".format(missing_keys)

    def get(self):
        return jsonify({}), HTTPStatusCodes.OK

    def post(self):
        """
            Function used to register a gateway with the initial information from the vendor
        :return:
        """
        body = request.json
        validation_error_message = self._validate_post_body(body)
        if validation_error_message:
            api.server.app.logger.error(
                "Some error occurred during the validation of the body. Reason: {}"
                    .format(validation_error_message)
            )
            response = {
                "message": validation_error_message
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        updated_rows = self.gateways_service.update(body["uuid"], body["name"], body["description"], body["ip"],
                                                    body["port"])
        if updated_rows:
            api.server.app.logger.debug("Gateway with uuid {} has already been registered".format(body["uuid"]))
            api.server.app.logger.debug("Updated Gateway info")
            response = {
                "message": "Gateways has been already registered. Update gateway info"
            }
            return jsonify(response), HTTPStatusCodes.CREATED

        gateway_data = {
            "uuid": body["uuid"],
            "name": body["name"],
            "description": body["description"],
            "ip": body["ip"],
            "port": body["port"],
        }
        _id = self.gateways_service.create(gateway_data)
        if not _id:
            response = {
                "message": "Failed to register the gateway. Regenerate the UUID"
            }
            # TODO: This may happen on a race condition
            return jsonify(response), HTTPStatusCodes.CONFLICT

        api.server.app.logger.info("Gateway {} has been registeredu")
        response = {
            "message": "Gateway has been register"
        }
        return jsonify(response), HTTPStatusCodes.CREATED
