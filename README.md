## To build the docker container:
```
docker build -t telephonish .\telephonish_be\
```

## To run the docker container:
```
docker-compose up
```


## Authentication Flow
#### Room Password Auth:
1. Room is created with or without a password
2. If room is created with a password, it is hashed and stored in DB.
3. When new players try to join, they submit a password.
4. If password is required on room, submitted password is checked against hash.
5. If passwords match, connection can continue.

#### Player Token Auth:
1. Websocket consumer generates player_token on connect, and stores it
2. After accepting connection, send player_token back to individual client
3. Token is stored by client, and sent with any future messages to authenticate the player.
4. Token is checked in websocket for any new messages before processing them.
