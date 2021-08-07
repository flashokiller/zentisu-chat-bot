print("[INFO]: INITIALIZING ...")
import re
from asyncio import (gather, get_event_loop, sleep)

from aiohttp import ClientSession
from pyrogram import (Client, filters, idle)
from Python_ARQ import ARQ

from config import *


print("[INFO]: INITIALIZING BOT CLIENT ...")
luna = Client(":memory:",
              bot_token=bot_token,
              api_id=api_id,
              api_hash=api_hash,
)
bot_id = int(bot_token.split(":")[0])
print("[INFO]: INITIALIZING ...")
arq = None


async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    if "Luna" in response:
        responsee = response.replace("Luna", "Kawaii Rika", "ZENTISU DEMON SLAYER")
    else:
        responsee = response
    if "Aco" in responsee:
        responsess = responsee.replace("Aco", "Rika","zentisu" )
    else:
        responsess = responsee
    if "Who is zentisu?" in responsess:
        responsess2 = responsess.replace("Who is zentisu?","Nani?👀")
    else:
        responsess2 = responsess
    await message.reply_text(responsess2)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command(["start", "start@zentisuchatbot"])
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}zentisu[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private
    & ~filters.command(["start", "start@zentisuchatbot"])
    & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        await message.reply_text("Ufff... ignoring ....")
        return
    await type_and_send(message)


@luna.on_message(filters.command(["start", "start@zentisuchatbot"]) & ~filters.edited)
async def startt(_, message):
    await message.reply_text("Hi, i'm alive:!")


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
    -----------------
  | Chatbot Started! |
    -----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
