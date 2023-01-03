#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor

from servicers.user import UserManager

import grpc
import user_pb2
import user_pb2_grpc

from grpc_reflection.v1alpha import reflection


def server():
    server = grpc.server(ThreadPoolExecutor(max_workers=2))

    user_pb2_grpc.add_UserManagerServicer_to_server(UserManager(), server)

    services = (reflection.SERVICE_NAME,)
    services += tuple(
        service.full_name for service in
        user_pb2.DESCRIPTOR.services_by_name.values()
    )
    reflection.enable_server_reflection(services, server)

    server.add_insecure_port('[::]:1234')

    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    try:
        server()
    except KeyboardInterrupt as e:
        print(e)
