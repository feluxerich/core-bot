from discord import Embed
from discord.ext.commands import Cog, command

from utils.bot import ExtendedBot
from utils.calculation_parser import Tokenizer


class CalculatorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(aliases=['calc'])
    async def calculate(self, ctx, *, calculation):
        parsed_calculation = Tokenizer(calculation).gen_tokens()
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

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CalculatorCog(client))
