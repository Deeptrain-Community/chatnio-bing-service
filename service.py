import json

from EdgeGPT.EdgeGPT import Chatbot
from EdgeGPT.conversation_style import CONVERSATION_STYLE_TYPE


async def create_chat_request(
        prompt: str,
        style: CONVERSATION_STYLE_TYPE,
        cookies: list[dict] | None,
        callback: callable,
) -> list[str]:
    instance = await Chatbot.create(cookies=cookies)
    resp = []
    async for final, response in instance.ask_stream(
            prompt=prompt,
            conversation_style=style,
    ):
        if not final:
            await callback(response)
        else:
            resp = json.loads(response)
            break
    await instance.close()

    return [segment.get('text') for segment in resp.get('suggestedResponses', [])]
