from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import uvicorn
import yaml
from fastapi import FastAPI, WebSocket
from task import run_task

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

    queue = Queue()
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(run_task, queue, content)
    while True:
        chunk = queue.get()
        if chunk is None:
            break

        await websocket.send_json({
            'response': chunk,
            'end': False,
        })

    await websocket.send_json({'response': '', 'end': True})
    await websocket.close()


if __name__ == "__main__":
    uvicorn.run(app, host=config['host'], port=config['port'])
