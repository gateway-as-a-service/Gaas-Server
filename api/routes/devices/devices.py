import api.server

from flask.views import MethodView
from flask import jsonify, request

from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_devices_service import DevicesService


class DevicesView(MethodView):
    POST_BODY_REQUIRED_FIELDS = {"id", "type", "name", "protocol", "gateway_uuid"}

    def __init__(self):
        self.devices_service = DevicesService()

    def _validate_post_body(self, body):
        if not isinstance(body, dict):
            return "Device registration info must be an object"

        missing_fields = self.POST_BODY_REQUIRED_FIELDS - body.keys()
        if missing_fields:
            return "Missing fields: {}".format(missing_fields)

    def get(self):
        pass

    def post(self):
        body = request.get_json()
        error_validation_message = self._validate_post_body(body)
        if error_validation_message:
            api.server.app.logger.error("Request body isn't valid. Reason: {}".format(error_validation_message))
            response = {
                "message": error_validation_message,
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        device_id = body["id"]
        gateway_uuid = body["gateway_uuid"]
        device = self.devices_service.find_device_from_gateway(device_id, gateway_uuid)
        if device:
            api.server.app.logger.error(
                "Do not register the device {} from gateway {} because it has been already registered"
                    .format(device_id, gateway_uuid)
            )
            response = {
                "message": "Device already registered",
            }
            return jsonify(response), HTTPStatusCodes.CONFLICT

        device__id = self.devices_service.create(body)
        response = {
            "_id": str(device__id),
        }
        return jsonify(response), HTTPStatusCodes.CREATED
