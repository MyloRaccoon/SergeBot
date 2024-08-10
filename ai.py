from characterai import aiocai
import asyncio

class AI:

    def __init__(self, char, client):
        self.char = char
        self.client = aiocai.Client(client)

    async def connect(self):
        self.me = await self.client.get_me()
        await self.new_chat()

    async def new_chat(self):
        async with await self.client.connect() as chat:
            self.chat = chat
            new, answer = await self.chat.new_chat(self.char, self.me.id)
            self.chat_id = new.chat_id

    async def send_serge(self, text : str, name : str):

        await self.client.edit_account(name=name)

        async with await self.client.connect() as chat:

            message = await chat.send_message(self.char, self.chat_id, text)

            return message.text

