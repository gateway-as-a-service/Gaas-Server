import api.server
from api.libs.exceptions import FailedRequestException
from api.libs.utils import MongoUtils


class DevicesService(object):
    def __init__(self):
        self.logger = api.server.app.logger
        self.devices_collection = MongoUtils.devices

    def create(self, device):
        try:
            return self \
                .devices_collection \
                .insert_one(device) \
                .inserted_id

        except Exception as err:
            self.logger.error(err)
            return None

    def find_from_gateway(self, gateway_uuid):
        try:
            return self.devices_collection \
                .find({"gateway_uuid": gateway_uuid}, {'_id': False})

        except Exception as err:
            self.logger.error("Failed to retrieve the devices that are part of gateway {}".format(gateway_uuid))
            raise FailedRequestException("Failed to retrieve the devices of the gateway")

    def find_multiple_devices(self, devices_ids):
        try:
            devices = self \
                .devices_collection \
                .find({"id": {"$in": devices_ids}})

            return devices

        except Exception as err:
            self.logger.error("Failed to retrieve the following devices : {}. Reason: {}".format(devices_ids, err))
            return []

    def find_device_from_gateway(self, device_uuid, gateway_uuid):
        try:
            return self \
                .devices_collection \
                .find_one({"id": device_uuid, "gateway_uuid": gateway_uuid})
        except Exception as err:
            self.logger.error(
                "Failed to retrieve the device {} that is part of gateway {}. Reason"
                    .format(device_uuid, gateway_uuid, err), exc_info=True
            )
            return None

    def update_device_value(self, device_id, new_device_value):
        try:
            return self.devices_collection \
                       .update_one({"id": device_id}, {"$set": {"value": new_device_value}}) \
                       .matched_count > 0

        except Exception as err:
            self.logger.error(
                "Failed to update the value of the device {}.Reason: {}"
                    .format(device_id, err), exc_info=True
            )
            raise FailedRequestException("Failed to update the value of the device")

    def update_multiple(self, device_id_to_value: dict):
        if not device_id_to_value:
            return 0

        updated_rows = 0
        for device_id, new_value in device_id_to_value.items():
            updated_rows += self.update_device_value(device_id, new_value)

        return updated_rows


if __name__ == '__main__':
    devices_service = DevicesService()
    print(
        devices_service.find_device_from_gateway(
            "0a9c8868-5ba4-4b18-bf92-320971118425",
            "09eb8a54-14cb-49cb-a374-de1da80ffb27"
        )
    )
