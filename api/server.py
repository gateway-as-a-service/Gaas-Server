from flask_cors import CORS

import api.libs.utils
from flask import Flask, jsonify

from api.configs.config import SERVER_NAME, SERVER_PORT, SERVER_HOST, SERVER_API_VERSION
from api.libs.exceptions import FailedRequestException
from api.routes.gateways.devices.devices import GatewaysDevicesView
from api.routes.devices.devices import DevicesView
from api.routes.devices.devices_actions import GatewaysDevicesActionsView
from api.routes.gateways.gateway_rules import GatewayRulesView
from api.routes.gateways.gateways import GatewaysView
from api.routes.users.users_fcm_tokens import UsersTokensView

app = Flask(SERVER_NAME)
CORS(app)
api.libs.utils.register_logger(app)


@app.errorhandler(FailedRequestException)
def handle_failed_request_exception(exception):
    return jsonify(exception.get_message()), exception.get_status_code()


devices_view = DevicesView.as_view("DevicesView")
gateways_view = GatewaysView.as_view("GatewaysView")
gateways_devices_actions_view = GatewaysDevicesActionsView.as_view("GatewaysDevicesActionsView")
gateways_devices_view = GatewaysDevicesView.as_view("GatewaysDevicesView")
gateways_rules_view = GatewayRulesView.as_view('GatewaysRulesView')
users_view = UsersTokensView.as_view("UsersView")

app.add_url_rule(
    rule="/api/{}/devices".format(SERVER_API_VERSION),
    view_func=devices_view,
    methods=["POST", ],
)

app.add_url_rule(
    rule="/api/{}/gateways".format(SERVER_API_VERSION),
    view_func=gateways_view,
    methods=["GET", "POST"],
)

app.add_url_rule(
    rule="/api/{}/gateways/<uuid:gateway_uuid>/devices/actions".format(SERVER_API_VERSION),
    view_func=gateways_devices_actions_view,
    methods=["POST", ],
)

app.add_url_rule(
    rule="/api/{}/gateways/<uuid:gateway_uuid>/devices".format(SERVER_API_VERSION),
    view_func=gateways_devices_view,
    methods=["GET", ],
    defaults={
        "device_uuid": None
    }
)

app.add_url_rule(
    rule="/api/{}/gateways/<uuid:gateway_uuid>/devices/<uuid:device_uuid>".format(SERVER_API_VERSION),
    view_func=gateways_devices_view,
    methods=["GET", "PATCH", ],
)

app.add_url_rule(
    rule="/api/{}/gateways/<uuid:gateway_uuid>/rules".format(SERVER_API_VERSION),
    view_func=gateways_rules_view,
    methods=["GET", "POST"]
)
app.add_url_rule(
    rule="/api/{}/gateways/<uuid:gateway_uuid>/rules/<string:rule_id>".format(SERVER_API_VERSION),
    view_func=gateways_rules_view,
    methods=["PUT"]
)

app.add_url_rule(
    rule="/api/{}/users/tokens".format(SERVER_API_VERSION),
    view_func=users_view,
    methods=["PUT", ],
)

if __name__ == '__main__':
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=True
    )
