from discord import Embed, Interaction
from discord.app_commands import command, describe
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.calculation_parser import Tokenizer
from utils.message import send


class CalculatorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='calculate', description='Do your homework :)')
    @describe(calculation='Your calculation string')
    async def calculate(self, interaction: Interaction, *, calculation: str):
        parsed_calculation = Tokenizer(calculation)()
        result: int | float = eval(''.join([token.value for token in parsed_calculation]))
        embed = Embed(
            title=self.client.config.EMBEDS['calculator']['title'],
            color=self.client.config.COLORS[self.client.config.EMBEDS['calculator']['color']]
        )
        format_keys = {
            'input': calculation,
            'result': result
        }
        for field in self.client.config.EMBEDS['calculator']['fields']:
            embed.add_field(
                name=self.client.config.EMBEDS['calculator']['fields'][field]['name'],
                value=self.client.config.EMBEDS['calculator']['fields'][field]['value'].format(**format_keys),
                inline=bool(self.client.config.EMBEDS['calculator']['fields'][field]['inline'])
            )

        await send(interaction=interaction, embed=embed)


async def setup(client: ExtendedBot):
    await client.add_cog(CalculatorCog(client), guild=client.DEFAULT_GUILD)
