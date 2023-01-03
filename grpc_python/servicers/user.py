from typing import List, Iterable
# from collections.abc import Iterable

from .database import init_table, get_all_users, get_user, add_user

import user_pb2
import user_pb2_grpc


init_table()

class UserManager(user_pb2_grpc.UserManagerServicer):

    def getUser(self, request: user_pb2.UserRequest, context):
        user = get_user(request.id)
        if not user:
            return user_pb2.UserResponse(error=True, message="not found")

        return user_pb2.UserResponse(error=False, user=user)

    def addUser(self, request: user_pb2.User, context):
        if get_user(request.id):
            return user_pb2.UserResponse(error=True, message="already exist")

        add_user(request)

        return user_pb2.UserResponse(error=False, user=request)

    def countAlreadyUsers(self, request_iter: Iterable[user_pb2.UserRequest], context):
        user_cnt = 0
        for request in request_iter:
            if get_user(request.id):
                user_cnt += 1

        return user_pb2.UserCntResponse(error=False, user_cnt=user_cnt)

    def getUsersByType(self, request: user_pb2.UserTypeRequest, context):
        user_type = user_pb2.User.UserType.Name(request.user_type)

        users = get_all_users()
        for user in users:
            if user_type == user_pb2.User.UserType.Name(user.user_type):
                yield user_pb2.UserResponse(error=False, user=user)

    def getUsersByIds(self, request_iter: Iterable[user_pb2.UserRequest], context):
        user_list = []
        for request in request_iter:
            user = get_user(request.id)
            if user:
                user_list.append(user)
        for user in user_list:
            yield user_pb2.UserResponse(error=False, user=user)
