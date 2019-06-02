from bson import ObjectId

import api.server
from api.libs.utils import MongoUtils


class UserService(object):

    def __init__(self):
        self.users_collection = MongoUtils.users

    def create(self, user):
        try:
            return self \
                .users_collection \
                .insert_one(user) \
                .inserted_id
        except Exception as err:
            api.server.app.logger.error(
                "Failed to create the user. Reason: {}".format(err)
            )
            return None

    def find(self, _id):
        try:
            return self.users_collection.find_one({"_id": ObjectId(_id)})
        except Exception as err:
            api.server.app.logger.error(
                "Failed to search after user with _id {}. Reason: {}"
                    .format(_id, err)
            )

    def update(self, user_id, **kwargs):
        new_values = {}
        if kwargs.get("fcm_token"):
            new_values["fcm_token"] = kwargs["fcm_token"]

        if not new_values:
            api.server.app.logger.info("No values provided")
            return True

        try:
            return self \
                       .users_collection \
                       .update_one({"_id": ObjectId(user_id)}, {"$set": new_values}) \
                       .matched_count > 0
        except Exception as err:
            api.server.app.logger.error(
                "Failed to update the user with the new values {}. Reason: {}"
                    .format(new_values, err)
            )
            return False


if __name__ == '__main__':
    user_service = UserService()
    user = {
        "name": "Ciprian",
        "gateways": [],
    }
    print(user_service.create(user))
