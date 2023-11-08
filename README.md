<div align="center">

# Chat Nio Bing Service
[ChatNio](https://github.com/Deeptrain-Community/chatnio) Bing Service

</div>

## Features
- [x] Bing Search
- [x] Websocket API
- [x] Authenticated
- [x] Multi-Threaded
- [x] Multi-Account Pool
- [x] Account Retry Feature

## Install
```shell
pip install -r requirements.txt
```

- save new bing cookies to `~/cookie.txt`
```shell
> cookies.txt
[
  [cookies],
  [cookies],
  ...
]
```

- configurate `config.yaml`

## API
[websocket] http://localhost:8765/chat

client sent:
```json
{
  "prompt": "string",
  "hash": "string (secret)",
  "model": "creative"
}
```

stream response:
```json
{
  "response": "string"
}
```
