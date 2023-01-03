from typing import List, Optional

import boto3

import json
from google.protobuf import json_format

from user_pb2 import User

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


def init_table():
    try:
        table = dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        print("table created")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        table = dynamodb.Table('users')

    table.meta.client.get_waiter('table_exists').wait(TableName='users')

    if table.item_count == 0:
        print("init table entries")

        init_db_file = "./json_data/users.json"
        with open(init_db_file, mode="r") as f:
            users = json.load(f)

        with table.batch_writer() as batch:
            for user_id, item in users.items():
                batch.put_item(Item=item)


def get_all_users() -> Optional[List[User]]:
    table = dynamodb.Table('users')
    response = table.scan()
    if 'Items' in response:
        users = response['Items']
        return [json_format.ParseDict(user, User()) for user in users]
    return None


def get_user(user_id: int) -> Optional[User]:
    table = dynamodb.Table('users')
    response = table.get_item(Key={"id": user_id})
    if 'Item' in response:
        user = response['Item']
        return json_format.ParseDict(user, User())
    return None


def add_user(user: User):
    table = dynamodb.Table('users')
    table.put_item(
        Item=json_format.MessageToDict(
            user, preserving_proto_field_name=True
        ))
