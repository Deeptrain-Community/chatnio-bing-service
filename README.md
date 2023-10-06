<div align="center">

# Chat Nio Bing Service
[ChatNio](https://github.com/Deeptrain-Community/chatnio) Bing Service

</div>

## Install
```shell
pip install -r requirements.txt
```

- save new bing cookies to `~/cookie.txt`
- configurate `config.yaml`

## API
[websocket] http://localhost:8765/chat

client sent:
```json
{
  "prompt": "string",
  "hash": "md5 string (prompt + config secret)",
  "model": "creative"
}
```

stream response:
```json
{
  "response": "string"
}
```
