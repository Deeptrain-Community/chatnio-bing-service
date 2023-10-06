import asyncio
import hashlib
import json
import websockets
import yaml
from service import create_chat

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


def validate_hash(prompt: str, _hash: str) -> bool:
    return hashlib.md5(prompt + config['secret']).hexdigest() == _hash


async def chat_handler(websocket, path):
    if path != '/chat':
        await websocket.close()
        return

    data = await websocket.recv()
    params = json.loads(data)
    prompt = params.get('prompt')
    model = params.get('model')
    if not validate_hash(prompt, params.get('hash')):
        await websocket.close()
        return

    async for data in create_chat(prompt=prompt, model=model):
        await websocket.send(json.dumps({'response': data, 'end': False}))

    await websocket.close()


if __name__ == "__main__":
    server = websockets.serve(chat_handler, config['host'], config['port'])
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
