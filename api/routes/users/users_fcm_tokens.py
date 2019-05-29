from flask.views import MethodView
from flask import jsonify
from flask import request

import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.users.users_service import UserService


class UsersFcmTokens(MethodView):
    POST_BODY_REQUIRED_FIELDS = {"token"}

    def __init__(self):
        self.logger = api.server.app.logger

        self.user_service = UserService()

    def _validate_post_body(self, body):
        if not isinstance(body, dict):
            return "Must provide an object"

        missing_fields = self.POST_BODY_REQUIRED_FIELDS - body.keys()
        if missing_fields:
            return "Missing fields: {}".format(missing_fields)

    def post(self):
        body = request.get_json()
        validation_error_message = self._validate_post_body(body)
        if validation_error_message:
            self.logger.error(
                "Some error occurred during the validation of the body. Reason: {}".format(validation_error_message)
            )
            response = {
                "message": validation_error_message,
            }
            return jsonify(response), HTTPStatusCodes.BAD_REQUEST

        fcm_token = body["token"]
        user_id = "5cef014dbc9e3b3638cde0e8" #TODO Remove the hardcode
        self.user_service.update(user_id, fcm_token=fcm_token)

        return jsonify({}), HTTPStatusCodes.NO_CONTENT
