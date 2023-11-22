from bing.virual import handle_request
from queue import Queue


def run_task(queue: Queue, content: str):
    for chunk in handle_request(content):
        queue.put(chunk)
    queue.put(None)
