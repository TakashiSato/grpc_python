from google.protobuf import json_format
from typing import List, Iterable
# from collections.abc import Iterable
import json

import user_pb2
import user_pb2_grpc


USER_DB = "./json_data/users.json"
with open(USER_DB, mode="r") as f:
    users = json.load(f)


class UserManager(user_pb2_grpc.UserManagerServicer):

    def getUser(self, request: user_pb2.UserRequest, context):
        user_id = str(request.id)

        if user_id not in users:
            return user_pb2.UserResponse(error=True, message="not found")
        user = users[user_id]

        result = json_format.ParseDict(user, user_pb2.User())
        # print(f"{result.user_type=}, {type(result.user_type)}")

        return user_pb2.UserResponse(error=False, user=result)

    def addUser(self, request: user_pb2.User, context):
        user_id = str(request.id)

        if user_id in users:
            return user_pb2.UserResponse(error=True, message="already exist")

        users[user_id] = json_format.MessageToDict(
            request, preserving_proto_field_name=True
        )
        with open(USER_DB, mode="w") as f:
            json.dump(users, f, indent=2, sort_keys=True)

        return user_pb2.UserResponse(error=False, user=request)

    def countAlreadyUsers(self, request_iter: Iterable[user_pb2.UserRequest], context):
        user_cnt = 0
        for request in request_iter:
            user_id = str(request.id)
            if user_id in users:
                user_cnt += 1

        return user_pb2.UserCntResponse(error=False, user_cnt=user_cnt)

    def getUsersByType(self, request: user_pb2.UserTypeRequest, context):
        user_type = user_pb2.User.UserType.Name(request.user_type)

        for user in users.values():
            if user_type == user["user_type"]:
                result = json_format.ParseDict(user, user_pb2.User())
                yield user_pb2.UserResponse(error=False, user=result)

    def getUsersByIds(self, request_iter: Iterable[user_pb2.UserRequest], context):
        user_list = []
        for request in request_iter:
            user_id = str(request.id)
            if user_id in users:
                user_list.append(users[user_id])
        for user in user_list:
            result = json_format.ParseDict(user, user_pb2.User())
            yield user_pb2.UserResponse(error=False, user=result)
