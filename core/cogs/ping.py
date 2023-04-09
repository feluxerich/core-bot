from discord import Embed, Interaction
from discord.app_commands import command
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.message import send


class PingCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='ping', description='Returns the current ping of the bot')
    async def ping(self, interaction: Interaction):
        await send(interaction=interaction, embed=Embed(
            title=self.client.config.EMBEDS['ping']['title'],
            description=self.client.config.EMBEDS['ping']['description'].format(ping=round(self.client.latency * 1000)),
            color=self.client.config.COLORS[self.client.config.EMBEDS['ping']['color']]
        ))


async def setup(client: ExtendedBot):
    await client.add_cog(PingCog(client), guild=client.DEFAULT_GUILD)
