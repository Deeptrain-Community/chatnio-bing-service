import asyncio
import json
import websockets
import yaml
from service import create_chat, init_client

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


async def chat_handler(websocket, path):
    try:
        if path != '/chat':
            await websocket.close()
            return

        data = await websocket.recv()
        params = json.loads(data)
        prompt = params.get('prompt')
        model = params.get('model')
        if not params.get('hash') == config['secret']:
            await websocket.close()
            return

        async for data in create_chat(prompt=prompt, model=model):
            await websocket.send(json.dumps({'response': data, 'end': False}))

        await websocket.send(json.dumps({'response': '', 'end': True}))
        await websocket.close()
    except Exception as e:
        print(e)


def run():
    server = websockets.serve(chat_handler, config['host'], config['port'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_client())
    loop.run_until_complete(server)
    loop.run_forever()


if __name__ == "__main__":
    run()
