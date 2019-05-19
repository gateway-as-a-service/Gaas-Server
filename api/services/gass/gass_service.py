import api.server
from api.configs.utils import HTTPStatusCodes
from api.services.gateways.gateways_service import GatewaysService

import requests


class GassService(object):

    def __init__(self):
        self.logger = api.server.app.logger

        self.gateway_service = GatewaysService()

    def send_device_update(self, gateway_uuid, device_uuid, body):
        gateway = self.gateway_service.find(uuid=gateway_uuid)
        if not gateway:
            self.logger.critical(
                "Failed to retrieve the gateway {} from DB. The performed actions will not be sent"
                    .format(gateway_uuid)
            )
            return False

        url = "{}/api/devices/{}".format(gateway["ip"], device_uuid)
        self.logger.info("Gateway URL: {}".format(url))
        try:
            response = requests.patch(url, json=body)
            if response.status_code == HTTPStatusCodes.NO_CONTENT:
                return True

            self.logger.warning(
                "Unexpected status code received: {} . Response: {}".format(response.status_code, response.text)
            )
            return False

        except Exception as err:
            self.logger.error("Failed to send to the gateway the performed actions")
            return False


if __name__ == '__main__':
    gass_service = GassService()
