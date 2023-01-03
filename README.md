# grpc_python

## setup

```
poetry install
```

## run dynamodb-local

```
docker-compose up --build
```

- you can view tables in http://localhost:8001/

## run grpc server

```
cd grpc_python
poetry shell
./grpc_server.py
```

## run grpc client by using python

```
cd grpc_python
poetry shell
./grpc_client.py getUser 1
---
user {
  id: 1
  nickname: "admin"
  mail_address: "admin@example.com"
  user_type: ADMINISTRATOR
}
```

## run grpc client by using evans
```
evans --host localhost -p 1234 -r
---
UserManager@localhost:1234> call getUser
id (TYPE_UINT32) => 1
{
  "user": {
    "id": 1,
    "mail_address": "admin@example.com",
    "nickname": "admin",
    "user_type": "ADMINISTRATOR"
  }
}
```

## references

- https://zenn.dev/kumamoto/articles/0596ed47f33965
- https://hackers-high.com/aws/dynamodb-local-development/
