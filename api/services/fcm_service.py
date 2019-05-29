from pyfcm import FCMNotification

import api.server
from api.configs.config import FCM_API_KEY


class FcmService(object):

    def __init__(self):
        self.logger = api.server.app.logger

        self.push_notification_service = FCMNotification(api_key=FCM_API_KEY)

    def _push_notification(self, registration_ids, device_id, device_value):
        message = {
            "title": "Test",
            "body": "It twarks",
            "click_action": "http://localhost:3000/",
            "icon": "http://url-to-an-icon/icon.png"
        }
        data = {
            "id": device_id,
            "value": device_value,
        }

        result = self.push_notification_service.notify_multiple_devices(
            registration_ids, message["body"], message["title"], message_icon=message["icon"],
            click_action=message["click_action"], data_message=data
        )
        self.logger.info("FCM push notification result: {}".format(result))
