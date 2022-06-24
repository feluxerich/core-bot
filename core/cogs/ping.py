from discord import Embed
from discord.ext.commands import Cog, command

from utils.bot import ExtendedBot
from utils.message import send


class PingCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(aliases=['p'])
    async def ping(self, ctx):
        await send(context=ctx, embed=Embed(
            title=self.client.config.EMBEDS['ping']['title'],
            description=self.client.config.EMBEDS['ping']['description'].format(ping=round(self.client.latency * 1000)),
            color=self.client.config.COLORS[self.client.config.EMBEDS['ping']['color']]
        ))


async def setup(client):
    await client.add_cog(PingCog(client))
