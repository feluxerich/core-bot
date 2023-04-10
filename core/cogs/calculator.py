from discord import Embed, Interaction
from discord.app_commands import command, describe
from discord.colour import parse_hex_number
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.calculation_parser import Tokenizer
from utils.message import send, make_embed


class CalculatorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='calculate', description='Do your homework :)')
    @describe(calculation='Your calculation string')
    async def calculate(self, interaction: Interaction, *, calculation: str):
        parsed_calculation = Tokenizer(calculation)()
        result: int | float = eval(''.join([token.value for token in parsed_calculation]))
        await send(
            interaction=interaction,
            embed=make_embed(self.client, 'calculator', input=calculation, result=result)
        )


async def setup(client: ExtendedBot):
    await client.add_cog(CalculatorCog(client), guild=client.DEFAULT_GUILD)
