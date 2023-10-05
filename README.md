<div align="center">

# Chat Nio Bing Service
[ChatNio](https://github.com/Deeptrain-Community/chatnio) Bing Service base on EdgeGPT

</div>

## API
[websocket] http://localhost:8765/chat

client sent:
```json
{
  "prompt": "string",
  "cookies": "list[dict]",
  "model": "creative"
}
```

stream response:
```json
{
  "response": "string",
  "suggested": "list[string] (optional)",
  "error": "string (optional)",
  "end": "bool"
}
```
