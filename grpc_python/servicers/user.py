from typing import List, Iterable
# from collections.abc import Iterable

from .database import init_table, get_all_users, get_user, add_user

from user_pb2 import (
    User, UserRequest, UserResponse,
    UserCntResponse,  UserTypeRequest
)
from user_pb2_grpc import UserManagerServicer


init_table()


class UserManager(UserManagerServicer):

    def getUser(self, request: UserRequest, context):
        user = get_user(request.id)
        if not user:
            return UserResponse(error=True, message="not found")

        return UserResponse(error=False, user=user)

    def addUser(self, request: User, context):
        if get_user(request.id):
            return UserResponse(error=True, message="already exist")

        add_user(request)

        return UserResponse(error=False, user=request)

    def countAlreadyUsers(self, request_iter: Iterable[UserRequest], context):
        user_cnt = 0
        for request in request_iter:
            if get_user(request.id):
                user_cnt += 1

        return UserCntResponse(error=False, user_cnt=user_cnt)

    def getUsersByType(self, request: UserTypeRequest, context):
        user_type = User.UserType.Name(request.user_type)

        users = get_all_users()
        for user in users:
            if user_type == User.UserType.Name(user.user_type):
                yield UserResponse(error=False, user=user)

    def getUsersByIds(self, request_iter: Iterable[UserRequest], context):
        user_list = []
        for request in request_iter:
            user = get_user(request.id)
            if user:
                user_list.append(user)
        for user in user_list:
            yield UserResponse(error=False, user=user)
