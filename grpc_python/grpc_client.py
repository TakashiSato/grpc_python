#!/usr/bin/env python3
from typing import List
from pprint import pprint
import sys

# 「grpc」パッケージと、protocによって生成したパッケージをimportする
import grpc
import user_pb2
import user_pb2_grpc


def get_user(stub, user_id: int):
    # リクエストに使用するオブジェクト（ここでは「UserRequest」型オブジェクト）を作成
    req = user_pb2.UserRequest(id=user_id)
    response = stub.getUser(req)
    # 取得したレスポンスの表示
    pprint(response)
    return response


def add_user(stub, user_id: int, nickname: str, mail_address: str, user_type: int):
    # リクエストに使用するオブジェクト（ここでは「User」型オブジェクト）を作成
    req = user_pb2.User(
        id=user_id, nickname=nickname, mail_address=mail_address, user_type=user_type
    )
    response = stub.addUser(req)
    # 取得したレスポンスの表示
    pprint(response)
    return response


def count_already_users(stub, user_id_list: List[int]):
    # リクエストに使用するオブジェクト（ここでは「UserRequest」型オブジェクト）を複数作成
    req_list = []
    for user_id in user_id_list:
        req = user_pb2.UserRequest(id=user_id)
        req_list.append(req)
    response = stub.countAlreadyUsers(iter(req_list))
    # 取得したレスポンスの表示
    pprint(response)
    return response


def get_users_by_type(stub, user_type: int):
    # リクエストに使用するオブジェクト（ここでは「UserTypeRequest」型オブジェクト）を作成
    req = user_pb2.UserTypeRequest(user_type=user_type)
    responses = stub.getUsersByType(req)
    response_list = []
    for r in responses:
        # 取得したレスポンスの表示
        pprint(r)  # debug
        response_list.append(r)
    return response_list


def get_users_by_ids(stub, user_id_list: List[int]):
    # リクエストに使用するオブジェクト（ここでは「UserRequest」型オブジェクト）を複数作成
    req_list = []
    for user_id in user_id_list:
        req = user_pb2.UserRequest(id=user_id)
        req_list.append(req)
    responses = stub.getUsersByIds(iter(req_list))
    response_list = []
    for r in responses:
        # 取得したレスポンスの表示
        pprint(r)  # debug
        response_list.append(r)
    return response_list


def main():
    # サーバーに接続する
    channel = grpc.insecure_channel("localhost:1234")
    # 送信先の「stub」を作成する
    stub = user_pb2_grpc.UserManagerStub(channel)
    # リクエストを送信する
    if sys.argv[1] == "getUser":
        res = get_user(stub=stub, user_id=int(sys.argv[2]))
    elif sys.argv[1] == "addUser":
        res = add_user(
            stub=stub,
            user_id=int(sys.argv[2]),
            nickname=sys.argv[3],
            mail_address=sys.argv[4],
            user_type=int(sys.argv[5]),
        )
    elif sys.argv[1] == "countAlreadyUsers":
        user_id_list = [int(sys.argv[2]), int(sys.argv[3])]
        res = count_already_users(stub=stub, user_id_list=user_id_list)
    elif sys.argv[1] == "getUsersByType":
        res = get_users_by_type(stub=stub, user_type=int(sys.argv[2]))
    elif sys.argv[1] == "getUsersByIds":
        user_id_list = [int(sys.argv[2]), int(sys.argv[3])]
        res = get_users_by_ids(stub=stub, user_id_list=user_id_list)
    return res


if __name__ == "__main__":
    main()
