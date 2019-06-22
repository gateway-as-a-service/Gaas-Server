from flask import jsonify
from flask import request
from flask.views import MethodView

import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.gass.gass_service import GassService
from api.services.gateways.gateways_devices_service import DevicesService
from api.services.gateways.gateways_service import GatewaysService
from api.services.gateways.gateways_rules_service import RulesService


class GatewaysDevicesView(MethodView):
    PATCH_BODY_REQUIRED_FIELDS = {"value"}

    def __init__(self):
        api.server.app.logger = api.server.app.logger

        self.devices_service = DevicesService()
        self.gateways_service = GatewaysService()
        self.rules_service = RulesService()

        self.gass_service = GassService()

    def _validate_patch_body(self, body):
        if not isinstance(body, dict):
            return "The body must be an object"

        missing_fields = self.PATCH_BODY_REQUIRED_FIELDS - body.keys()
        if missing_fields:
            return "Missing fields: {}".format(missing_fields)

    def _retrieve_devices(self, gateway_uuid):
        devices = self.devices_service.find_from_gateway(gateway_uuid)
        response = {
            "devices": list(devices)
        }
        return jsonify(response), HTTPStatusCodes.OK

    def _retrieve_device(self, gateway_uuid, device_uuid):
        device = self.devices_service.find_device_from_gateway(device_uuid, gateway_uuid)
        if not device:
            api.server.app.logger.warning(
                "Device {} doesn't exists or it isn't part of gateway {}".format(device_uuid, gateway_uuid)
            )
            response = {
                "message": "Device wasn't found or isn't part of the gateway"
            }
            return jsonify(response), HTTPStatusCodes.NOT_FOUND

        device.pop("_id", None)
        return jsonify(device), HTTPStatusCodes.OK

    def get(self, gateway_uuid, device_uuid):
        if not device_uuid:
            return self._retrieve_devices(str(gateway_uuid))

        return self._retrieve_device(str(gateway_uuid), str(device_uuid))

    # TODO: Add Gateway permissions access (JWT Token)
    # TODO: Implement control access to the gateways
    def patch(self, gateway_uuid, device_uuid):
        body = request.get_json()
        validation_error_message = self._validate_patch_body(body)
        if validation_error_message:
            api.server.app.logger.error(
                "Some error occurred during the validation of the body. Reason: {}".format(validation_error_message)
            )
            response = {
                "message": validation_error_message,
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        device_uuid = str(device_uuid)
        gateway_uuid = str(gateway_uuid)
        device = self.devices_service.find_device_from_gateway(device_uuid, gateway_uuid)
        if not device:
            api.server.app.logger.warning(
                "Device {} doesn't exists or it isn't part of gateway {}".format(device_uuid, gateway_uuid)
            )

        message_to_gateway = {
            "value": body["value"]
        }
        sent = self.gass_service.send_device_update(gateway_uuid, device_uuid, message_to_gateway)
        if not sent:
            response = {
                "message": "Failed to send the request to the gateway because wasn't found"
            }
            return jsonify(response), HTTPStatusCodes.NOT_FOUND

        api.server.app.logger.info("Sent message to gateway")
        return jsonify({}), HTTPStatusCodes.NO_CONTENT
