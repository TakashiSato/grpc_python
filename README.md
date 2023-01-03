# grpc_python

## setup

```
poetry install
```

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