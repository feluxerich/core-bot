from discord import Interaction, Embed, Color
from discord.app_commands import command
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.message import send, make_embed


class MiscCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='help', description='Returns this help')
    async def help(self, interaction: Interaction):
        cogs = [cog for cog in self.client.cogs.keys() if cog not in ['EventsCog', 'ReactionRoleCog']]
        description = ''
        for cog in cogs:
            cog_help_string = f'**{cog[:-3]}**\n'
            cog_help_string += '\n'.join(
                [f'`{i.name}` - {i.description}' for i in self.client.get_cog(cog).get_app_commands()]
            )
            description += f'{cog_help_string}\n\n'
        await send(interaction=interaction, embed=Embed(
            title='Help',
            description=description,
            color=Color.from_str(self.client.config.COLORS['pink'])
        ))

    @command(name='ping', description='Returns the current ping of the bot')
    async def ping(self, interaction: Interaction):
        await send(
            interaction=interaction,
            embed=make_embed(self.client, 'ping', ping=round(self.client.latency * 1000))
        )


async def setup(client: ExtendedBot):
    await client.add_cog(MiscCog(client), guild=client.DEFAULT_GUILD)
