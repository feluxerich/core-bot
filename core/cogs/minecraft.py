from datetime import datetime

from aiohttp import ClientSession
from discord import Interaction
from discord.app_commands import command, describe
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.message import send, make_embed


class MinecraftCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='uuid', description='Returns the Minecraft UUID to a given player')
    @describe(username='The Minecraft player\'s username')
    async def uuid(self, interaction: Interaction, username: str):
        async with ClientSession() as session, session.get(
                f'https://api.mojang.com/users/profiles/minecraft/{username}') as resp:
            output = await resp.json()
            await send(
                interaction=interaction,
                embed=make_embed(self.client, 'minecraft', username=username, content=output['id'])
            )


async def setup(client: ExtendedBot):
    await client.add_cog(MinecraftCog(client), guild=client.DEFAULT_GUILD)
