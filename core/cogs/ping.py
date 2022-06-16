from discord import Embed
from discord.ext.commands import Cog, command

from utils.bot import ExtendedBot


class PingCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(aliases=['p'])
    async def ping(self, ctx):
        await ctx.send(embed=Embed(
            title=self.client.config.EMBEDS['ping']['title'],
            description=self.client.config.EMBEDS['ping']['description'].format(round(self.client.latency * 1000)),
            color=self.client.config.COLORS[self.client.config.EMBEDS['ping']['color']]
        ))


def setup(client):
    client.add_cog(PingCog(client))
