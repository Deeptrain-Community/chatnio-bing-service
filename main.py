import asyncio
import json
import websockets
from service import create_chat_request


async def chat_handler(websocket, path):
    if path != '/chat':
        await websocket.close()
        return

    try:
        data = await websocket.recv()
        params = json.loads(data)
        prompt = params.get('prompt')
        model = params.get('model')
        cookies = params.get('cookies')
        cursor = 0

        async def process_response(response: str):
            nonlocal cursor
            cursor = len(response)
            await websocket.send(json.dumps({'response': response[cursor:], 'end': False}))

        try:
            suggest = await create_chat_request(prompt=prompt, model=model, cookies=cookies, callback=process_response)
            await websocket.send(json.dumps({'suggested': suggest, 'response': '', 'end': True}))
        except Exception as e:
            await websocket.send(json.dumps({'error': f'bing error: {str(e)}', 'response': '', 'end': True}))

        await websocket.close()
    except Exception as e:
        print(f"WebSocket Error: {e}")


if __name__ == "__main__":
    server = websockets.serve(chat_handler, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
