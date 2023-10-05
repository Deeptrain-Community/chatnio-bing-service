import json

from EdgeGPT.EdgeGPT import Chatbot
from EdgeGPT.conversation_style import CONVERSATION_STYLE_TYPE, ConversationStyle

STYLES = {
    "creative": ConversationStyle.creative,
    "balanced": ConversationStyle.balanced,
    "precise": ConversationStyle.precise,
}


async def create_chat_request(
        prompt: str,
        model: str,
        cookies: list[dict] | None,
        callback: callable,
) -> list[str]:
    instance = await Chatbot.create(cookies=cookies)
    style: CONVERSATION_STYLE_TYPE = STYLES.get(model, ConversationStyle.creative)
    suggest = []

    async for final, response in instance.ask_stream(
            prompt=prompt,
            conversation_style=style,
    ):
        if not final:
            await callback(response)
        else:
            suggest = json.loads(response)
            break
    await instance.close()

    return [segment.get('text') for segment in suggest.get('suggestedResponses', [])]
