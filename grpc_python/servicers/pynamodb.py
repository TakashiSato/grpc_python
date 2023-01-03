from typing import List, Optional
import logging

import json
from google.protobuf import json_format

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import PutError

from user_pb2 import User


class UserModel(Model):
    class Meta:
        host = "http://localhost:8000"
        table_name = 'users'
        region = 'ap-northeast-1'
        read_capacity_units = 1
        write_capacity_units = 1

    id = NumberAttribute(hash_key=True)
    mail_address = UnicodeAttribute(null=True)
    nickname = UnicodeAttribute(null=True)
    user_type = UnicodeAttribute(null=True)


def init_table():
    if not UserModel.exists():
        UserModel.create_table(wait=True)
        print("table created")

    if UserModel.count() == 0:
        print("init table entries")

        init_db_file = "./json_data/users.json"
        with open(init_db_file, mode="r") as f:
            users = json.load(f)

        for user_id, item in users.items():
            new_user = UserModel(**item)
            new_user.save()


def get_all_users() -> Optional[List[User]]:
    users = UserModel.scan()
    return [json_format.Parse(user.to_json(), User()) for user in users]


def get_user(user_id: int) -> Optional[User]:
    try:
        user = UserModel.get(user_id)
        return json_format.Parse(user.to_json(), User())
    except UserModel.DoesNotExist as e:
        logging.error(f'Unable to get user: {e}')
        return None


def add_user(user: User):
    new_user = UserModel(
        **(json_format.MessageToDict(
            user, preserving_proto_field_name=True
    )))

    try:
        new_user.save(UserModel.id.does_not_exist())
    except PutError as e:
        logging.error(f'Unable to add user: {e}')
