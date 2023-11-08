import asyncio
import json
import os
import random

from async_bing_client import *

with open('cookie.json', 'r') as file:
    cookie = json.load(file)

clients = [
    Bing_Client(cookie=segment, proxy=os.environ.get('http_proxy', None) or os.environ.get('https_proxy', None))
    for segment in cookie
]

STYLES = {
    "creative": ConversationStyle.Creative,
    "balanced": ConversationStyle.Balanced,
    "precise": ConversationStyle.Precise,
}


def getSnippet(snippet: str) -> str:
    length = len(snippet)
    return snippet if length < 80 else snippet[:80] + "..."


def getSearchResult(data: SearchResult) -> str:
    if isinstance(data.content, list):
        result = ""
        for outer_index, each in enumerate(data.content):
            result += f"\n({outer_index + 1}) {each.get('title')}:\n"
            for index, snippet in enumerate(each['snippets']):
                result += f"[{index + 1}]: {getSnippet(snippet)}\n"
        return f'{result}\n'
    else:
        return data.content


async def create_chat(prompt: str, model: str, retry: int = 0):
    instance = random.choice(clients)
    try:
        chat = await instance.create_chat()
        sources = []
        suggest_reply = []
        images = []
        limit = None
        style = STYLES.get(model, ConversationStyle.Creative)
        async for data in instance.ask_stream_raw(prompt, None, chat=chat, conversation_style=style):
            if isinstance(data, Text):
                yield data.content
            elif isinstance(data, SuggestRely):
                suggest_reply.append(data)
            elif isinstance(data, SourceAttribution):
                sources.append(data)
            elif isinstance(data, Apology):
                yield '\n' + data.content
            elif isinstance(data, Image):
                images.append(data)
            elif isinstance(data, Limit):
                limit = data
            elif isinstance(data, SearchResult):
                yield getSearchResult(data)
        for index, source in enumerate(sources):
            if index == 0:
                yield "\n\n*See more:*\n"
            yield f"{index + 1}. {source}  \n"
        for index, image in enumerate(images):
            if index == 0:
                yield "\n\n"
            yield f"{image}\n"
        for index, reply in enumerate(suggest_reply):
            if index == 0:
                yield "\n*Suggested Reply:*\n"
            yield f"- {reply.content}\n"
        if limit and limit.num_user_messages > limit.max_num_user_messages:
            yield "\nYou have reached the limit of the number of messages you can send. Please try again tomorrow."
    except Exception as e:
        if retry >= 3:
            yield f'bing error: {e}'
        else:
            print(f'bing error: {e}, retry {retry + 1} times')
            async for data in create_chat(prompt, model, retry + 1):
                yield data


async def init_client():
    for instance in clients:
        await instance.init()
