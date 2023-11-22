import uvicorn
import yaml
from fastapi import FastAPI, WebSocket

from bing.virual import handle_request

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

app = FastAPI()


@app.websocket_route("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()

    if not data.get('hash') == config['secret']:
        await websocket.close()
        return

    content = data.get('prompt', '')

    async for chunk in handle_request(content):
        await websocket.send_json({
            'response': chunk,
            'end': False,
        })

    await websocket.send_json({'response': '', 'end': True})
    await websocket.close()


if __name__ == "__main__":
    uvicorn.run(app, host=config['host'], port=config['port'])
