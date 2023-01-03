import grpc
import hello_pb2
import hello_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:8000') as channel:
        stub = hello_pb2_grpc.HelloWorldStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='Yamada'))
    print(f"RECV: {response.message}")


if __name__ == '__main__':
    run()
