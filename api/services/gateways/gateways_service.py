from bson import ObjectId

import api.server
from api.libs.exceptions import FailedRequestException
from api.libs.utils import MongoUtils


class GatewaysService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.gateways_collection = MongoUtils.gateways

    def create(self, gateway):
        try:
            return self \
                .gateways_collection \
                .insert_one(gateway) \
                .inserted_id
        except Exception as err:
            self.logger.error("Failed to create the gateway. Reason: {}".format(err), exc_info=True)
            return None

    def find(self, _id=None, uuid=None):
        criteria = {}
        if _id:
            criteria["_id"] = ObjectId(_id)

        if uuid:
            criteria["uuid"] = uuid

        if not criteria:
            return None

        try:
            return self \
                .gateways_collection \
                .find_one(criteria)
        except Exception as err:
            self.logger.error(
                "Failed to retrieve the gateway with id {}. Reason: {}"
                    .format(_id, err), exc_info=True
            )
            raise FailedRequestException("Failed to retrieve the gateway")

    def update(self, gateway_uuid, name=None, description=None, ip=None, port=None):
        new_values = {}
        if name:
            new_values["name"] = name

        if description:
            new_values["description"] = description

        if ip:
            new_values["ip"] = ip

        if port:
            new_values["port"] = port

        if not new_values:
            return 0

        try:
            return self.gateways_collection \
                       .update_one({"uuid": gateway_uuid}, {"$set": new_values}) \
                       .matched_count > 0

        except Exception as err:
            self.logger.error(
                "Failed to update info about gateway: {}. Reason: {}"
                    .format(gateway_uuid, err), exc_info=True
            )


if __name__ == '__main__':
    gateway_service = GatewaysService()
    print(gateway_service.find(uuid='e1799142-0430-48f4-9b5d-1348591c0bf7'))
    print(gateway_service.update('e1799142-0430-48f4-9b5d-1348591c0bf7'))
