from discord import Interaction
from discord.app_commands import command
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.message import send, make_embed


class PingCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='ping', description='Returns the current ping of the bot')
    async def ping(self, interaction: Interaction):
        await send(
            interaction=interaction,
            embed=make_embed(self.client, 'ping', ping=round(self.client.latency * 1000))
        )


async def setup(client: ExtendedBot):
    await client.add_cog(PingCog(client), guild=client.DEFAULT_GUILD)
