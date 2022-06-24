from discord import Embed
from discord.ext.commands import Cog, command

from utils.bot import ExtendedBot
from utils.calculation_parser import Tokenizer
from utils.message import send


class CalculatorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(aliases=['calc'])
    async def calculate(self, ctx, *, calculation):
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

        await send(context=ctx, embed=embed)


async def setup(client):
    await client.add_cog(CalculatorCog(client))
